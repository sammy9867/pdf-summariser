def get_session_id_from_request(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    return session_id
