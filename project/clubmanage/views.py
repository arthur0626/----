# main/views.py
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def user_view(request):
    search_query = request.GET.get('search_query', '')  # 검색어
    search_type = request.GET.get('search_type', 'name')  # 검색 타입 (기본값은 'name')

    joined_data = []

    # 검색어와 검색 타입을 프로시저에 전달하여 결과 가져오기
    with connection.cursor() as cursor:
        cursor.callproc('search_user_records', [search_query, search_type])
        joined_data = cursor.fetchall()  # 프로시저 결과 가져오기
    
    context = {
        'joined_data': joined_data,  # 프로시저 결과 전달
        'search_query': search_query,  # 현재 검색어 전달
        'search_type': search_type,    # 현재 검색 타입 전달
    }
    return render(request, 'user.html', context)

def team_view(request):
    search_query = request.GET.get('search_query', '')  # 검색어
    search_type = request.GET.get('search_type', 'name')  # 검색 타입 (기본값은 'name')

    joined_data = []

    # 검색어와 검색 타입을 프로시저에 전달하여 결과 가져오기
    with connection.cursor() as cursor:
        cursor.callproc('search_team_records', [search_query, search_type])
        joined_data = cursor.fetchall()  # 프로시저 결과 가져오기
    
    context = {
        'joined_data': joined_data,  # 프로시저 결과 전달
        'search_query': search_query,  # 현재 검색어 전달
        'search_type': search_type,    # 현재 검색 타입 전달
    }
    return render(request, 'team.html', context)
DEFAULT_PASSWORD = "0000"  # 초기 비밀번호 설정

def user_add_view(request):
    if request.method == "POST":
        try:
            # 작업 타입 확인
            action_type = request.POST.get("type")

            # 비밀번호 확인
            input_password = request.POST.get("password")
            if input_password != DEFAULT_PASSWORD:
                messages.error(request, "비밀번호가 틀립니다.")
                return render(request, "user_add.html")

            # 학번 확인 (필수)
            student_id = request.POST.get("student_id")
            if not student_id:
                messages.error(request, "학번을 입력하세요.")
                return render(request, "user_add.html")

            # 추가 작업
            if action_type == "add":
                user_data = {
                    "name": request.POST.get("name"),
                    "age": request.POST.get("age"),
                    "major": request.POST.get("major"),
                    "contact": request.POST.get("contact"),
                    "genres": request.POST.getlist("genres"),
                    "available_days": request.POST.getlist("available_days"),
                    "sessions": request.POST.getlist("sessions"),
                }
                with connection.cursor() as cursor:
                    # 기본 사용자 정보 추가
                    cursor.callproc("add_user_and_get_id", [
                        student_id,
                        user_data["name"],
                        int(user_data["age"]),
                        user_data["major"],
                        user_data["contact"],
                    ])
                    cursor.execute("SELECT @last_user_id")
                    user_id = cursor.fetchone()[0]

                    # 선호 장르 추가
                    cursor.callproc("add_user_genres", [
                        user_id,
                        *["k_pop" in user_data["genres"],
                          "j_pop" in user_data["genres"],
                          "pop" in user_data["genres"],
                          "hard" in user_data["genres"],
                          "indie" in user_data["genres"],
                          "funk" in user_data["genres"],
                          "r_b" in user_data["genres"],
                          "ballad" in user_data["genres"]]
                    ])

                    # 가능 요일 추가
                    cursor.callproc("add_user_available_days", [
                        user_id,
                        *["mon" in user_data["available_days"],
                          "tue" in user_data["available_days"],
                          "wed" in user_data["available_days"],
                          "thu" in user_data["available_days"],
                          "fri" in user_data["available_days"],
                          "sat" in user_data["available_days"],
                          "sun" in user_data["available_days"]]
                    ])

                    # 세션 추가
                    cursor.callproc("add_user_sessions", [
                        user_id,
                        *[2 if session in user_data["sessions"] else 1
                          for session in ["vocal", "guitar", "bass", "drum", "keyboard"]]
                    ])

            # 변경 작업
            elif action_type == "update":
                user_data = {
                    "name": request.POST.get("name"),
                    "age": request.POST.get("age"),
                    "major": request.POST.get("major"),
                    "contact": request.POST.get("contact"),
                }
                with connection.cursor() as cursor:
                    cursor.callproc("update_user_by_id", [
                        student_id,
                        user_data["name"],
                        int(user_data["age"]),
                        user_data["major"],
                        user_data["contact"],
                    ])

            # 삭제 작업
            elif action_type == "delete":
                with connection.cursor() as cursor:
                    cursor.callproc("delete_user_by_id", [student_id])

            messages.success(request, f"{action_type} 작업 성공!")
            return redirect("user")

        except Exception as e:
            messages.error(request, f"오류 발생: {str(e)}")
            return redirect("user")

    return render(request, "user_add.html")


def team_edit_view(request):
    if request.method == "POST":
        action_type = request.POST.get("type")
        input_password = request.POST.get("password")

        # 비밀번호 확인
        if input_password != DEFAULT_PASSWORD:
            messages.error(request, "비밀번호가 틀립니다.")
            return render(request, "team_edit.html")

        team_data = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "song1": request.POST.get("song1"),
            "song2": request.POST.get("song2"),
            "song3": request.POST.get("song3"),
            "song4": request.POST.get("song4"),
            "song5": request.POST.get("song5"),
            "time": request.POST.get("time"),
            "vocal": request.POST.get("vocal"),
            "second_vocal": request.POST.get("second_vocal"),
            "guitar": request.POST.get("guitar"),
            "second_guitar": request.POST.get("second_guitar"),
            "third_guitar": request.POST.get("third_guitar"),
            "bass": request.POST.get("bass"),
            "drum": request.POST.get("drum"),
            "keyboard": request.POST.get("keyboard"),
            "second_keyboard": request.POST.get("second_keyboard"),
        }

        with connection.cursor() as cursor:
            # 추가 작업
            if action_type == "add":
                cursor.callproc("add_team", [
                    team_data["name"],
                    team_data["description"],
                    team_data["song1"],
                    team_data["song2"],
                    team_data["song3"],
                    team_data["song4"],
                    team_data["song5"],
                    team_data["time"],
                    team_data["vocal"],
                    team_data["second_vocal"],
                    team_data["guitar"],
                    team_data["second_guitar"],
                    team_data["third_guitar"],
                    team_data["bass"],
                    team_data["drum"],
                    team_data["keyboard"],
                    team_data["second_keyboard"],
                ])
                messages.success(request, "팀이 추가되었습니다.")

            elif action_type == "update":
                cursor.callproc("update_team", [
                    team_data["name"],
                    team_data["description"],
                    team_data["song1"],
                    team_data["song2"],
                    team_data["song3"],
                    team_data["song4"],
                    team_data["song5"],
                    team_data["time"],
                    team_data["vocal"],
                    team_data["second_vocal"],
                    team_data["guitar"],
                    team_data["second_guitar"],
                    team_data["third_guitar"],
                    team_data["bass"],
                    team_data["drum"],
                    team_data["keyboard"],
                    team_data["second_keyboard"],
                ])
                messages.success(request, "팀이 업데이트되었습니다.")

            elif action_type == "delete":
                cursor.callproc("delete_team", [team_data["name"]])
                messages.success(request, "팀이 삭제되었습니다.")
                
            return redirect('team')

    return render(request, "team_edit.html")