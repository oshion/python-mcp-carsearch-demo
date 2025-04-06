# Car Database MCP Server

이 프로젝트는 자동차 데이터베이스를 MCP(Model Context Protocol) 서버로 노출하는 애플리케이션입니다. LLM(Large Language Model)이 자동차 데이터베이스에 접근하여 검색, 조회 및 추천 기능을 사용할 수 있게 합니다.

## 데모
https://nest-resource-bucket.s3.ap-northeast-2.amazonaws.com/MCP_local_demo.mp4

## 기능

- 조건에 맞는 자동차 검색
- 특정 자동차의 상세 정보 조회
- 사용 가능한 검색 파라미터 조회
- 브랜드별 모델 목록 조회
- 사용자 선호도에 따른 검색 파라미터 추천

## 설치

1. 필요한 의존성 설치:

```bash
pip install -r requirements.txt