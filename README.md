## Naming convention

> Formatter로 Python의 black을 사용 합니다. 

### Apps
- app directory 명은 lowercase를 따릅니다.

### Model
- model의 변수들은 snake_case 규칙을 따릅니다.
- model의 상수 값들은 UPPER_CASE 규칙을 따릅니다. 
- Foreign Key를 사용하는 필드의 related_name은 모델 클래스 명의 복수 형태를 snake_case로 변환한 형태로 표기합니다. [공식 문서의 예제](https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ManyToManyField.through_fields)