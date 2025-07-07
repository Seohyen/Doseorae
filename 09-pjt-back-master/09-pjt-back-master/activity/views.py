import openai
from decouple import config

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
import json

API_KEY = config('API_KEY')
openai.api_key = API_KEY

@api_view(['POST'])
def ask_gpt(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

    content = (
        "당신은 감성분석 전문가이자 책 전문가입니다.\n"
        f"사용자가 다음과 같은 감정을 표현했습니다: \"{prompt}\"\n"
        "이 감정을 바탕으로, 사용자에게 깊은 공감과 위로를 줄 수 있는 책 5권을 추천해주세요.\n"
        "각 책에 대해 제목, 저자, 간단한 추천 이유를 포함해 주세요. 응답 데이터에 마크다운 문법은 없어야 합니다.  " 
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}]
    )
    return Response(response.choices[0].message.content)

@api_view(['POST'])
def quizeGpt(request):
    bookName = request.data.get("bookName", "")
    if not bookName:
        return Response({"error": "bookName is required"}, status=status.HTTP_400_BAD_REQUEST)

    prompt = (
        f"당신은 교육 전문가입니다.\n"
        f"다음 책 '{bookName}'의 내용을 기반으로 객관식 퀴즈를 3문제 출제해주세요.\n"
        "각 퀴즈는 다음 조건을 반드시 지켜야 합니다:\n"
        "- 문제는 명확하고 간결해야 합니다.\n"
        "- 선택지는 4개이며, 각각 A, B, C, D로 표기합니다.\n"
        "- 정답은 단일 선택지여야 하며, 복수 정답은 허용하지 않습니다.\n"
        "- 결과를 JSON 배열 형식으로 아래와 같이 정확히 반환해주세요:\n"
        """[
    {
        "question": "...",
        "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
        "answer": "A"
    },
    {
        "question": "...",
        "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
        "answer": "B"
    },
    {
        "question": "...",
        "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
        "answer": "C"
    }
]"""
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 JSON 배열 형식으로만 응답하는 교육 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        quizzes = json.loads(content)
    except json.JSONDecodeError:
        print("GPT 응답 파싱 실패:", content)
        return Response({"error": "GPT 응답 JSON 파싱 실패", "raw": content}, status=500)

    return Response(quizzes)


@api_view(['POST'])
def debateGpt(request):
    bookName = request.data.get("bookName", "")
    prompt = request.data.get("prompt", "")
    if not bookName or not prompt:
        return Response({"error": "bookName and prompt are required"}, status=status.HTTP_400_BAD_REQUEST)

    if prompt == "start":
        content = f"'{bookName}에 대한 토론을 시작하겠습니다.' 라고 답변하세요" 
    else: 
        content = (
            f"당신은 논리적 사고에 능한 토론 전문가입니다.\n"
            f"책 '{bookName}'에서 다음 주제에 대해 설명한 내용을 바탕으로, "
            f"사용자가 제시한 주장 '{prompt}'에 대해 논리적이고 설득력 있게 반박하는 답변을 작성해 주세요.\n"
            "답변은 정중하면서도 명확한 근거를 포함해야 하며, 간결하게 작성해 주세요."
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}]
    )
    return Response(response.choices[0].message.content)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def updatePlayerLevel(request):
    user = request.user
    user.exp += 20
    
    while user.exp >= user.maxExp:
        user.level += 1
        user.exp -= user.maxExp
        user.maxExp = int(user.maxExp * 1.5)
    user.save()
    return Response(status=status.HTTP_200_OK)