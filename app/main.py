import pymysql
from typing import List, Dict, Optional
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import asyncio

# 서버 생성
mcp = FastMCP(name="Car Database Server", instructions="이 서버는 자동차 데이터베이스에 대한 검색 및 조회 기능을 제공합니다.")


@dataclass
class Car:
    """자동차 정보를 담는 데이터 클래스"""
    id: int
    brand: str  # 브랜드
    model: str  # 모델명
    year: int  # 연식
    color: str  # 색상
    mileage: int  # 주행거리 (km)
    price: int  # 가격 (원)
    car_type: str  # 차종 (경차, 소형차, 중형차, 대형차)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'mileage': self.mileage,
            'price': self.price,
            'car_type': self.car_type
        }



def get_db_config():
    # 환경 변수 또는 config 파일에서 설정 가져오기
    try:
        import config
        return {
            'host': config.DB_HOST,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'db': config.DB_NAME,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
    except ImportError:
        # config 파일이 없는 경우 환경 변수 직접 사용
        import os
        return {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'user': os.environ.get('DB_USER', 'car'),
            'password': os.environ.get('DB_PASSWORD', 'test'),
            'db': os.environ.get('DB_NAME', 'car_db'),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }



def connect_db():
    """데이터베이스에 연결하는 메서드"""
    return pymysql.connect(**get_db_config())


# 자동차 관련 도구들을 담는 클래스
class CarTools:
    @mcp.tool(name="search_cars",
              description="사용자가 지정한 조건(연식, 색상, 주행거리, 가격, 차종, 브랜드 등)에 맞는 자동차 목록을 검색합니다. 검색 결과는 ID, 브랜드, 모델, 연식, 색상, 주행거리, 가격, 차종 정보를 포함합니다.")
    def search_cars(
            self,
            min_year: Optional[int] = None,
            max_year: Optional[int] = None,
            color: Optional[str] = None,
            max_mileage: Optional[int] = None,
            min_price: Optional[int] = None,
            max_price: Optional[int] = None,
            car_type: Optional[str] = None,
            brand: Optional[str] = None
    ) -> List[Dict]:
        """
        주어진 조건에 맞는 자동차 목록을 검색합니다.

        Args:
            min_year: 최소 연식 (예: 2018)
            max_year: 최대 연식 (예: 2022)
            color: 색상 (예: '흰색', '검정색', '빨간색')
            max_mileage: 최대 주행거리 (km)
            min_price: 최소 가격 (원)
            max_price: 최대 가격 (원)
            car_type: 차종 (경차, 소형차, 중형차, 대형차)
            brand: 브랜드 (예: '현대', '기아', 'BMW')

        Returns:
            조건에 맞는 자동차 목록
        """
        connection = connect_db()

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 생성
                query = "SELECT * FROM cars WHERE 1=1"
                params = []

                # 조건 추가
                if min_year:
                    query += " AND year >= %s"
                    params.append(min_year)

                if max_year:
                    query += " AND year <= %s"
                    params.append(max_year)

                if color:
                    query += " AND color = %s"
                    params.append(color)

                if max_mileage:
                    query += " AND mileage <= %s"
                    params.append(max_mileage)

                if min_price:
                    query += " AND price >= %s"
                    params.append(min_price)

                if max_price:
                    query += " AND price <= %s"
                    params.append(max_price)

                if car_type:
                    query += " AND car_type = %s"
                    params.append(car_type)

                if brand:
                    query += " AND brand = %s"
                    params.append(brand)

                # 쿼리 실행
                cursor.execute(query, params)
                result = cursor.fetchall()

                # 결과를 Car 객체 리스트로 변환
                cars = [Car(
                    id=row['id'],
                    brand=row['brand'],
                    model=row['model'],
                    year=row['year'],
                    color=row['color'],
                    mileage=row['mileage'],
                    price=row['price'],
                    car_type=row['car_type']
                ).to_dict() for row in result]

                return cars
        finally:
            connection.close()

    @mcp.tool(name="select_car",
              description="자동차 ID를 기반으로 특정 차량의 상세 정보를 조회합니다. 선택한 차량의 브랜드, 모델, 연식, 색상, 주행거리, 가격, 차종 등 모든 정보를 반환합니다.")
    def select_car(self, car_id: int) -> Dict:
        """
        선택한 자동차의 상세 정보를 가져옵니다.

        Args:
            car_id: 자동차 ID

        Returns:
            선택한 자동차의 상세 정보
        """
        connection = connect_db()

        try:
            with connection.cursor() as cursor:
                # SQL 쿼리 실행
                cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
                result = cursor.fetchone()

                if not result:
                    raise ValueError(f"ID {car_id}인 자동차를 찾을 수 없습니다.")

                # Car 객체로 변환
                car = Car(
                    id=result['id'],
                    brand=result['brand'],
                    model=result['model'],
                    year=result['year'],
                    color=result['color'],
                    mileage=result['mileage'],
                    price=result['price'],
                    car_type=result['car_type']
                )

                return {
                    "message": f"{car.brand} {car.model}을(를) 선택하셨습니다. 좋은 선택입니다!",
                    "car": car.to_dict()
                }
        finally:
            connection.close()

    @mcp.tool(name="get_available_parameters",
              description="차량 검색에 사용할 수 있는 모든 파라미터 값을 조회합니다. 브랜드, 색상, 차종 목록과 연식, 가격, 주행거리의 범위를 반환합니다. 이 정보를 통해 사용자는 검색 조건을 정확하게 지정할 수 있습니다.")
    def get_available_parameters(self) -> Dict:
        """
        차량 검색에 사용할 수 있는 모든 파라미터 값들을 조회합니다.

        Returns:
            각 컬럼별 사용 가능한 값들의 목록
        """
        connection = connect_db()

        try:
            with connection.cursor() as cursor:
                parameters = {}

                # 브랜드 목록 조회
                cursor.execute("SELECT DISTINCT brand FROM cars ORDER BY brand")
                parameters['brands'] = [row['brand'] for row in cursor.fetchall()]

                # 색상 목록 조회
                cursor.execute("SELECT DISTINCT color FROM cars ORDER BY color")
                parameters['colors'] = [row['color'] for row in cursor.fetchall()]

                # 차종 목록 조회
                cursor.execute("SELECT DISTINCT car_type FROM cars ORDER BY car_type")
                parameters['car_types'] = [row['car_type'] for row in cursor.fetchall()]

                # 연식 범위 조회
                cursor.execute("SELECT MIN(year) as min_year, MAX(year) as max_year FROM cars")
                year_range = cursor.fetchone()
                parameters['year_range'] = {
                    'min': year_range['min_year'],
                    'max': year_range['max_year']
                }

                # 가격 범위 조회
                cursor.execute("SELECT MIN(price) as min_price, MAX(price) as max_price FROM cars")
                price_range = cursor.fetchone()
                parameters['price_range'] = {
                    'min': price_range['min_price'],
                    'max': price_range['max_price']
                }

                # 주행거리 범위 조회
                cursor.execute("SELECT MIN(mileage) as min_mileage, MAX(mileage) as max_mileage FROM cars")
                mileage_range = cursor.fetchone()
                parameters['mileage_range'] = {
                    'min': mileage_range['min_mileage'],
                    'max': mileage_range['max_mileage']
                }

                return parameters
        finally:
            connection.close()

    @mcp.tool(name="get_models_by_brand",
              description="특정 브랜드에 속한 모든 자동차 모델 목록을 조회합니다. 브랜드를 입력으로 받아 해당 브랜드에서 제공하는 모든 모델명을 알파벳순으로 정렬하여 반환합니다.")
    def get_models_by_brand(self, brand: str) -> List[str]:
        """
        특정 브랜드의 사용 가능한 모델 목록을 조회합니다.

        Args:
            brand: 자동차 브랜드 이름

        Returns:
            해당 브랜드의 모델 목록
        """
        connection = connect_db()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT model FROM cars WHERE brand = %s ORDER BY model", (brand,))
                models = [row['model'] for row in cursor.fetchall()]
                return models
        finally:
            connection.close()

    @mcp.tool(name="recommend_search_parameters",
              description="사용자 선호도에 따라 최적의 차량 검색 파라미터를 추천합니다. '경제적', '고급', '실용적', '스포티'와 같은 선호도 키워드를 입력받아 해당 특성에 맞는 검색 파라미터를 제안합니다.")
    def recommend_search_parameters(self, preference: str) -> Dict:
        """
        사용자 선호도에 따른 검색 파라미터 추천

        Args:
            preference: 사용자 선호도 (예: '경제적', '고급', '실용적', '스포티')

        Returns:
            추천 검색 파라미터
        """
        if preference.lower() == '경제적':
            return {
                'max_price': 3000000,
                'min_year': 2018,  # 비교적 최신 모델
                'car_type': '경차'
            }
        elif preference.lower() == '고급':
            return {
                'min_price': 5000000,
                'brands': ['BMW', '벤츠', '아우디'],
                'min_year': 2020
            }
        elif preference.lower() == '실용적':
            return {
                'car_type': '소형차',
                'max_mileage': 50000,
                'min_year': 2019
            }
        elif preference.lower() == '스포티':
            return {
                'car_type': '스포츠카',
                'colors': ['빨간색', '검정색']
            }
        else:
            # 기본 추천
            return {
                'min_year': 2020,
                'max_mileage': 70000
            }


# 클래스 인스턴스 생성
car_tools = CarTools()


# 서버 실행 코드 추가
async def main():
    # 서버 실행 (stdio 또는 SSE 선택)
    # mcp.run(transport="stdio")
    # SSE로 실행하려면 아래 코드 사용
    mcp.run(transport="sse")


# 스크립트가 직접 실행될 때만 서버 실행
if __name__ == "__main__":
    asyncio.run(main())