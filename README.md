# dyros_mobile_model
Kim Hyoung Cheol (kimhc37@snu.ac.kr)
2021.06.23

### 실험 환경
- Ubuntu 18.04
- numpy-stl `pip install numpy-stl`
- PyYaml `pip install pyYAML`
- MeshLab `sudo snap install meshlab` (생성된 stl 파일 확인용)
### aml_reader.py
aml 파일은 도대체 언제적 형식일까... 이를 좀더 보기 좋게 만들기 위해 yaml 형식으로 변경해주는 코드이다. 다만 우리의 모델 파일 외의 파일은 잘 변형을 안해줄것이라 믿는다. 맞춤제작이 되었기 때문에.
test_out.yaml 파일을 만들어준다.
### stl_maker.py
aml_reader.py에서 생성된 파일을 읽어와 stl 파일을 제작한다.
추가로 stl_info.yaml과 stl_info_no_vertex.yaml 파일을 만들어준다. 중간에 확인하는 과정에서 vertex 정보 때문에 가독성이 떨어지는 부분이 있어 추가로 vertex 정보가 없는 파일도 만들게 했다.
### stl_modifier.py
이전 aml 파일에 있는 mesh들의 경우 부품별로 작게작게 다 나뉘어 있었다. 모델링의 편의를 위해 몇몇 mesh들을 하나로 묶어서 제작하게 만드는 코드이다.
aml 파일에 있는 vertex 정보들은 이미 transform이 적용된 점들의 위치이기 때문에 약간의 transform을 통해 원점을 기준으로 stl 파일이 제작되도록 했다.

['011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '032', '033']
위와같은 번호를 가진 mesh를 하나의 mesh로 통합했다.

### URDF
dyros_mobile.urdf 파일을 CoppeliaSim에서 import해 시뮬레이션 scene제작을 진행했다.
다만 import를 하는 과정에서 회전(rpy)의 반영이 되지 않아 이상하게 만들어진 부분이 있어 CoppeliaSim 상에서 추가적인 수정을 진행했다.
그렇기 때문에 URDF 모델과 CoppeliaSim 모델의 축 선언이 다르게 되어있는 상태임. 추후에 수정할 예정이다.

xacro.urdf로 끝나는 파일들의 경우 확인을 하지 않았기 때문에 잘못된 정보가 들어있을 것이다.
