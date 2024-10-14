2024/10/14
목표 : 로키 유지 시스템을 만들자

기술 스택
1. 클래스 & 클래스 다이어그램(UML)
2. 상속
3. 추상클래스
4. 클래스 설계
5. 다형성
6. 클래스변수 vs 인스턴스 변수


시나리오
    공장장 관리자(사용자) : 철수씨
    사용 목표 : 하나의 컨트롤러로 로봇의 모든 부품, 작동 현황을 보고 받고 조종할 수 있다.
    Use case :
        [ 주요 기능 ]
            로봇 클래스
                - 관리자는 로봇의 작동 현황을 알 수 있다. :
                    - 로봇의 현재 작동 상태 표시 (active)
                    - 로봇의 현재 작동 상품 표시 (current_product)
                    - 로봇의 제작 가능한 상품 표시 (product)
                    - 로봇의 현재 작동 상품의 제작 시간 표시/ 제작 시간(current_pruduct_time / pruduct_time)
                    - 로봇의 현재 소프트웨어 버전 표시 (version)

                - 관리자는 주요 부품의 상세 정보를 알 수 있다. :
                    - 로봇의 부품 조립 현황 (part_dog, part_cat, part_apple로 A,B,C가 있다.)
                    - 로봇 부품 수명 예측양( 현재 상품 생산 갯수로 표현) (parts_lifespan_prediction)
                        -- 로봇의 상품에 따른 부품들의 마모도(parts_wear_level)
                    - 로봇 부품 고장 상태 표시 (failure_state)
                
                - 관리자가 명령을 내리면 상품을 만들어 옮긴다.
                    - 상품 제작 함수
                    - 고장 부품 수리 함수
                    - 컨트롤러에 데이터 주고 받기 가능, 쓰레드(위의 상태를 주고 받도록)

            로봇 제어 컨트롤러
                - 관리자는 컨트롤러를 통해 로봇을 제어할 수 있다. : ()
                    - UI 데이터를 보내는 함수
                    - 컨트롤러 제어하는 함수(제어해서 로봇이 작동해 상품 제작하도록,)
                    - 로봇 작동 시키는 함수(작동 후 ACK를 받아 일정 확인 가능)
                    - 로봇 상태 가져오는 함수
                    - 로봇 상품 라인 변경시키는 함수
                    - 로봇 부품 고치는 함수
                    - 로봇과 데이터 주고 받을 수 있는 쓰레드
                    - 컨트롤러를 만들고, 로봇을 만들어서, 라인, 프로세스를 만드는 게 가능한 함수(라인 생성 함수, 제거 함수)

                - 관리자는 컨트롤러를 통해 로봇의 소프트웨어를 제어할 수 있다. : (softwareUpdate)
                    - 위에서 작성한, 만들고 제거하는 함수를 통해 주기적인 백업이 가능(일정 시간마다 파일 저장),
                    - 소프트웨어 업데이트의 경우, 구현하기 애매하므로 그냥 버전으로만 확인하기

                - 관리자는 컨트롤러를 보고 있지 않더라도 이메일을 통해 설비 상태를 보고 받을 수 있다. (email)
                    - 고장이 났을 시, 적혀있는 메일로 해당 라인, 로봇, 부품의 고장 알림
                    - 일정 시간시 설비 상태 보고 메일 날림
                    
코드 컨벤션
    - 로봇 클래스의 경우, robot_ 로 시작한다.
    - 로봇 클래스의 경우, 각각 factory, line, process 로 나눈다.
    - 컨트롤러 클래스의 경우, controller_ 로 시작한다.
    - 컨트롤러 간 사이, 컨트롤러와 로봇사이의 데이터는 json으로 준다.
    - 공정에서 상품생산시 시간을 무조건 지킨다.