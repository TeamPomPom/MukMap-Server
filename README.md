## Commit convention
- 영어로 커밋 메세지를 작성 한다면, 명령어로 작성 하도록 합니다.
- 최대한 작업의 의미 단위로 쪼개서 커밋 해주세요.

## Pull Request convention
- PR의 제목은, milestone 버전 명으로 시작 해주세요 ( ex_ milestone 1.0에 관련된 PR이라면, M1.0 또는 milestone 1.0 등으로 시작 해주세요 )

## Naming convention
> Formatter로 Python의 black을 사용 합니다. 

### Apps
- 하나의 django application에는, 하나의 주제만 담기도록 구축하는 것을 원칙으로 합니다.
- ex_ 유저와 유저가 구독한 유튜버들에 대한 데이터들은 유저에 속할 수 있지만 ( ManyToMany관계로 ), 유튜버와 유저는 둘 다 어느 하나에 속할 수 없으므로 앱을 분리합니다.
- app directory 명은 lowercase를 따릅니다.

### Model
- model의 변수들은 snake_case 규칙을 따릅니다.
- model의 상수 값들은 UPPER_CASE 규칙을 따릅니다. 
- Foreign Key를 사용하는 필드의 related_name은 모델 클래스 명의 복수 형태를 snake_case로 변환한 형태로 표기합니다. [공식 문서의 예제](https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ManyToManyField.through_fields)
- db_table 명을 항상 지정 해주시고, 테이블 명은 snake_case 규칙을 따릅니다. 

## Project structure
- 범용적으로 사용 가능하고, 각 앱들에 종속되지 않는 클래스는 config / core에 생성 해 주시면 됩니다. (ex_ authentication.py, SoftDeletionModel ... )
- 범용적으로 사용 가능하나 각 앱들에 종속되는 클래스는 각 앱에 생성 해 주시면 됩니다. (ex_ apps/permissions.py & apps/validates.py ... )