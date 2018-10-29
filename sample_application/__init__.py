from flask import Flask, render_template, flash, g
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from flask import request
import flask_sijax
import random
import json


qa_set = {
    0:(
        '''구 상무는 겸손하고 소탈한 성격인 것으로 알려져 있다. 실제 동료 직원들과 격의없이 소통하는 등 소탈하게 지내지만, 업무에서는 강한 실행력과 통찰력을 보여주고 있다는 평가를 받고 있다. 미국에서 유학 중이던 2000년대 중반, 한 여인을 만나 사랑에 빠졌다고 한다. 그녀의 이름은 정효정. 중소기업 보락의 정기련 대표의 장녀이다. 주변인에 따르면 효정 씨는 성격이 원만하고 매사에 성실해 친구들 사이에서 단연 인기가 좋았다고 한다. 혼인 이야기가 시작되면서 처음 보락 측에서 굴지의 재벌가와 사돈이 되는 것에 큰 부담을 가졌다. 그러나 LG에서 두 사람의 만남을 지원하고 나서며 두 사람은 2009년 결혼에 성공하였다.''',
        '구 상무가 미국에서 유학 중 사랑에 빠진 그녀의 이름은?',
        '정효정',
        '정효정'
        ),
    1:(
        '''1962년에 동생 구정회가 사장직에 취임한 후 그해 라디오를 처음으로 미국 아이젠버그 사에 수출했고, 1963년에 최초로 국산 적산전력량계도 개발해냈다. 1964년 부산 온천동에 종합전기기기공장을 개설하고 연지동 시대를 마감했다. 1965년 4월에 최초로 국산 냉장고를 만들고 실업기술원양성소를 세운 뒤, 그리고 1966년 8월 최초의 국산 19인치 흑백텔레비전 VD-191를 생산하며 일약 한국 우량 전자회사로 입지를 굳혔고, 이후 대한전선, 삼성 등 후발 업체들의 진출에 영향을 주었다.''',
        '최초의 국산 흑백텔레비전은?',
        'VD-191',
        'VD-191'
        ),
    2:(
        '''고글은 일반적인 상황 외의 시야 확보를 위한 아주 중요한 도구이다. 낮에는 눈(snow) 으로부터 반사되는 자외선으로부터 눈(eyes)을 보호하는 역할을 하나, 그렇다고 해서 '밤에는 착용하지 않아도 괜찮겠지?' 라고 생각해서는 안된다. 눈보라도 있다. 바람이 불지 않아도 타 스키어/보더가 턴을 하면서 지나갈 때 날리는 눈보라를 막지 않으면 자연스레 시야가 차단되게 되고 이는 곧 어마어마한 사고를 초래할 수 있다. 만약 안경을 쓰고 있다면 콘택트 렌즈를 이용하거나 안경을 덮을 수 있는 큰 사이즈의 고글을 착용하면 된다. 특히 콘택트 렌즈를 쓸 경우 고글이 없으면 눈으로 바람이 들어와 눈물이 나고, 앞이 잘 안 보이게 된다.''',
        '시야 확보를 위한 중요한 도구는?',
        '고글',
        '고글'
         ),
    3:(
        '''2014년부터 국제탁구연맹은 공의 재질을 셀룰로이드에서 플라스틱으로 바꾸었다. 이 플라스틱 공을 일반적으로 폴리볼이라 부르는데 기존의 셀룰로이드 볼과 같이 두 조각을 이어 붙여 이음매가 존재하는 형태와 통째로 사출하여 이음매 없는 버전 모두 공인되어 사용되고 있다. 유럽에서는 폴리볼이 2014년 초에 바로 도입이 되었지만 아시아권에서는 유럽보다 늦은 2014년 인천 아시안 게임 이후 본격적인 사용이 이루어지게 되었다. 메이커 별로 어느정도 차이는 있지만 기존 셀룰로이드 볼에 비해서 회전이 잘 걸리지 않는다는 평이 대다수다(이제는 플라스틱공만을 경기에서 쓰도록 바뀌었다. 117년만에 공의 재질이 바뀌는 것인데, 그 이유는 기존의 셀룰로이드를 태울 때 나오는 독성 때문이다. ''',
        '117년만에 공의 재질이 바뀐 것은 셀룰로이드를 태울 때 나오는 무엇 때문인가?',
        '독성',
        '독성'
        ),
    4:(
        '''세계탁구는 크게 동양권과 유럽권 두 계열로 분류되는데 1980년대 말부터 1990년대 초에는 남자는 유럽권, 여자는 동양권이 선전했지만 1990년대 중반 이후에는 남녀 모두 동양권, 특히 중국이 압도적인 강세다[3]. 1952년에 탁구를 도입한 이래 탁구를 전 인민들에게 보급하고 연구를 통해 독자적인 용구와 기술을 개발하는 등 지원을 아끼지 않았으며, 덕분에 현재 중국 탁구 선수들의 실력은 매우 뛰어난 편이다.. 다르게는 만리장성. 그 좋은 예로 우승만 132번을 기록한 탁구 마녀 덩야핑(鄧亞萍)이 있다. 중국 내에서는 등록선수가 무려 2,000만~3,000만 명이라고 하며, 한국에 PC방이 많은 것처럼 중국에서는 어디를 가나 탁구대가 많다. 올림픽에선 중국이 메달을 독식하는 것을 막기 위해 국가별로 출전 인원 제한이 있으나 오히려 이 때문에 올림픽이 다른 세계 대회보다 더 경쟁력이 떨어진다고 하는 선수들도 일부 있다.''',
        '탁구 마녀 덩야핑은 우승을 몇 번 하였는가?',
        '132번',
        '132번'
        ),
    5:(
        '''레벨이 오르면 챔피언의 각 능력치가 일정량 늘어나며 이를 '성장 스탯'이라 한다. 즉, 챔피언이 레벨을 올리게 되면 체력, 체력 재생, 마나, 마나 재생, 공격력, 공격 속도, 방어력, 마법 저항력이 종합적으로 상승하게 된다. 또한 레벨이 오를 때마다 스킬 포인트를 하나씩 상승시킬 수 있게 된다. 1레벨부터 궁극기를 사용할 수 있거나 궁극기라는 개념이 존재하지 않는 일부 챔피언들을 제외하면 일반적으로 궁극기는 6레벨에 배울 수 있으며, 11레벨과 16레벨에 각각 궁극기를 강화[4]시킬 수 있다. 그리고 성장 스탯의 경우, 레벨이 오를 때마다 선형적으로 증가하지 않는다. 예를 들어 성장 공격력이 3이라면 경기 초반에는 레벨업을 하더라도 공격력이 3보다 적게 오른다. 대신 10레벨을 넘게 되면 레벨업을 할 경우 공격력이 3보다 많이 오르게 되어, 결국 18레벨이 되면 1레벨에 비해 3 x 17 = 51만큼의 공격력을 추가적으로 획득하게 된다.''',
        '일반적으로 궁극기는 언제 배울 수 있는가?',
        '6레벨',
        '6레벨'
        ),
    6:(
        '''터치라인의 길이는 100~130야드(91.44m~118.87m)이고 국제경기용은 110~120야드(100.58m~109.73m)이다. 골라인의 길이는 50~100야드(45.72m~91.44m)이고 국제경기용은 70~80(64.01m~73.15m)야드이다. 반드시 터치라인이 골라인보다 길어야 한다. 다시 말해 100야드 x 100야드는 불가능. 터치라인과 골라인의 길이를 105미터 68미터로 하는 안이 정해졌었으나 현재까지 시행은 보류되고 있다. 골에어리어는 20야드 6야드. 골 에어리어 내에서는 골킥의 위치를 자유롭게 택해서 찰 수 있고 수비측의 프리킥도 자유롭게 위치를 선정할 수 있다. 페널티에어리어는 18야드~44야드 이다. 이 안에서 프리킥에 해당하는 반칙은 페널티 킥으로 업글된다. 또한 골키퍼가 손으로 공을 다룰 수 있는 있는 한계영역이다. 페널티마크는 골라인 가운데로부터 12야드 지점에 표시한다.  페널티에어리어 바깥에 있는 반원은 페널티아크라고 부르며 페널티마크에서 반지름 10야드의 반원형태로 그린다. 센터라인 가운데 센터마크를 표시하고 반지름 10야드의 원을 그린다.''',
        '페널티에어리어는 몇 야드인가?',
        '18야드~44야드',
        '18야드~44야드'
        ),
    7:(
        '''대한민국에서는 야구도 인기가 많지만 축구 역시 인기가 많은 스포츠라고 볼 수 있다. 야구, 농구, 배구와 함께 대한민국의 4대 스포츠 중 하나로 꼽히고 있다. 1980년대에 차범근이 독일 분데스리가에서 명성을 떨치기도 하였고, 대한민국 최상위 프로축구 리그이자, 아시아 최고리그인 K리그는 1983년에 슈퍼리그로 출범하면서 지금까지도 프로리그가 이어지고 있으며, 현재까지 AFC 챔피언스 리그 우승 횟수가 가장 많은 리그이기도 하다. 대한축구협회의 인프라 구축과 더불어 공만 있으면 어디든지 즐길 수 있다는 간편함 때문에 조기축구회는 아마추어 스포츠 팀 중 가장 큰 규모를 자랑하고 생활 스포츠의 저변에서는 여전히 1위를 달리는 종목이다. 과거 차범근 이후 그리고 2002년 월드컵을 거치면서 해외 리그에 대한 관심도 박지성, 손흥민 같은 해외파가 등장하면서 급증했고, 중고등학교의 축구부나 아마추어 리그 팀이 현재 대한민국 내의 다른 스포츠들과는 비교도 안 될 정도로 많다. ''',
        'AFC 챔피언스 리그 우승 횟수가 가장 많은 리그는 언제 슈퍼리그로 출범하였는가?',
        '1983년',
        '1983년'
        ),
    8:(
        '''상원의원의 임기는 6년이며, 본래는 주 의회에서 상원의원을 간선으로 선출했는데, 1914년 수정헌법으로 인해 2년마다 50개주 중 1/3씩 연방 상원의원을 새로 선출하여 연방에 보내는 것으로 바뀌었다. 연방의회 직할 행정구인 수도 워싱턴 D.C.에는 상원의원 선출권이 없다. 그래서 워싱턴의 시민들은 자동차 번호판에 'No Taxation without Representation'이라는 항의 문구를 달고 다니면서 불만을 표시하기도 한다. 미국의 의회에만 상원의원만 있는 것이 아니라 각 주 의회에도 네브래스카 주를 제외한 모든 주에 상원이 있고 상원의원이 있다. 예를 들면 버락 오바마 전 대통령은 미 의회 상원의원이 되기 전에 일리노이 주 의회 상원의원이었고, 지미 카터 전 대통령은 조지아 주 의회 상원의원을 거쳐 조지아 주지사를 역임하고 대통령이 되었으며, 프랭클린 루스벨트 전 대통령은 뉴욕 주 의회 상원의원을 거쳐 뉴욕 주지사를 역임하고 대통령이 되었고, 캘빈 쿨리지 전 대통령은 메사추세츠 주 의회 상원의원이었다가 의장을 역임하고 부주지사와 주지사를 거쳐 부통령, 대통령이 되었다.''',
        '조지아 출신의 대통령은?',
        '지미 카터',
        '지미 카터'
        ),
    9:(
        '''쿠엔틴 타란티노의 특징이라면 극단적인 폭력성, B급 성향, 찰진 수다, 과거 영화에 대한 오마쥬, 탁월한 음악 선곡 능력 등이 꼽히고, 이 외에도 극단적인 성향의 캐릭터들의 충돌, 장황하지만 시시껄렁한 대사들, 긴장감 넘치는 서스펜스 등을 특징으로 가지고 있다. 타란티노는 대사와 입담, 촘촘히 쌓아올리는 복선과 이야기, 복선과 긴장감이 모여서 일어나는 순간적인 폭발이 장기라고 할 수 있다. 따라서 타란티노의 작품들은 B급 영화라기보다는 B급의 향취를 갖고 있는 A급 블랙 코미디에 가깝다. 특히 B급 영화라기에는 대사가 무척 길고 많으며, 대사가 내포하는 의미나 사용되는 말장난도 매우 수준 높다. 피와 폭력에 대한 집착은 유명한데 자기 영화 제작사의 사명이 장뤼크 고다르의 느와르물 《부외자들》이며 피칠갑 일본 영화 《코로시야 이치》에 광희하여 이 영화의 배우 세 명을 섭외하여 《킬빌》에 출연시키기도 했다.''',
        '타란티노가 영향을 받은 영화가 제작된 국가는 어디인가?',
        '일본',
        '일본'
        ),
    10:(
        '''광역버스는 물론이고 경기도에 출입하는 시계외버스는 서울을 통과하는 지점을 기준으로 하여 번호가 부여된다. 예를 들어 똑같이 성남에서 출발하는 시내버스라도 장지동을 경유해서 들어오는 버스는 3이(302, 303 등), 내곡동을 경유해서 들어오는 버스는 4가(407, 440 등) 붙는다. 은평구나 마포구를 거쳐 고양시 및 파주시로 빠지면 당연히 7번이 붙는다. 또한 경기도-서울을 오가는 노선들은 아무리 굴곡이 적고 거리가 길더라도 0권역에 진입하지 않는 이상은 전부 지선버스 노선으로 분류하였으며 0권역에 진입하는 노선들은 간선버스로 분류하였다. 다만 광역버스가 간선버스로 형간전환될 경우에는 보통 간선/지선버스들의 규칙을 적용받지 않고 출발 권역 번호가 그대로 유지된다. 여기서 더 예외인 케이스는 541번인데, 과천에서 우면지구로 서울로 진입할 때 처음 닿는 자치구가 서초구이기 때문에 4를 적용받게 되지만(과거 4425번) 5를 가져갔다. 이건 같은 회사의 다른 노선들(441, 540)과 번호가 비슷하게 보이게 유도해서 신규노선 홍보 효과를 좀 더 많이 노려보려는 의도도 다분히 있다. 사실 541번은 개편 전에 좌석버스로 처음 시작한 노선이다.''',
        '홍보 효과를 위해 일반적인 노선 규칙에서 벗어난 번호를 부여받은 버스는 몇 번인가?',
        '541번',
        '541번'
        ),
    11:(
        '''주 무대는 뉴욕 맨해튼에 위치한 가상의 거리 세서미 스트리트로, 123번지의 아파트를 중심으로 거리의 이웃들의 이야기를 다룬다. 평화로운 농가나 숲속, 환상의 나라 등을 주로 배경으로 하는 아동물의 규칙을 깨고, 현실적인 도심의 이야기를 전달하기 위해 뉴욕을 배경으로 설정한 것은 혁신적이라는 평가를 받고 있다. 인형 외에 등장하는 인간 배우들 역시, 뽀미언니 같은 교육자형 캐릭터가 아니라 가게 주인 같은 현실적인 이웃사람들의 캐릭터를 취하고 있으며 이들과 머펫들의 드라마 역시 볼거리이다. 방영 시작 당시부터 히스패닉 등 유색인종 이민자 캐릭터들이 등장하여, 차별이 남아있던 일부 주에서는 방영 금지가 되기도 하였다. 실제 청각장애인인 배우가 귀가 안 들리는 도서관 사서로 등장하여 큰 화제가 되었으며, 다른 배우들까지 수화를 배우며 방송에 참여한 사실은 레전드. 아이들에게 수화와 청각장애에 대해서 가르쳐주기 위해서였다고. 실제로 손동작만으로 의사소통하는 모습은 당시의 어린이들에게 건전한 컬쳐쇼크를 주었다. 주 등장인물인 인형들은 각양각색의 다양한 디자인을 취하고 있으며 성격도 개성이 풍부한데, 이는 아이들에게 인종이나 생각이 다른 사람들이라도 화합하고 서로 도우며 살아갈 수 있다는 것을 보여주기 위해서이다.''',
        '장애인 배우가 맡은 역할은 무엇인가?',
        '도서관 사서',
        '도서관 사서'
        ),
    12:(
        '''로버트의 죽음 이후 수많은 영주들이 왕을 자처하며 일어서고 다섯 왕의 전쟁이 일어난다. 로버트의 죽음 이후 왕에 오른 왕비의 아들 조프리 바라테온. 근친으로 낳은 아들들은 왕이 될 수 없으니 자신이 정당한 계승자임을 주장하는 로버트의 첫째 동생이자 좁은 해역의 왕 스타니스 바라테온, 구금된 아버지를 구출하고 북부와 리버랜드를 독립시키려는 북부의 왕 롭 스타크, 높은 인망으로 남부의 지지를 받는 로버트의 둘째 동생이자 하이 가든의 왕 렌리 바라테온, 혼란을 틈타 강철 군도의 힘을 한데 모아 웨스테로스로 진출하려는 소금과 암초의 왕 발론 그레이조이. 한편 타르가리옌 가문의 마지막 후예인 비세리스 타르가리옌은 바다 건너 에소스 대륙으로 도망쳐 도트락인들의 우두머리인 칼 드로고와 여동생 대너리스 타르가리옌을 결혼시켜 강력한 군대를 얻고 다시 왕좌를 되찾으려 한다. 장벽 너머에는 전설 속의 존재인 백귀들이 부활했다는 소문이 돌고, 만스 레이더는 와일들링들을 규합하여 백귀들과 여름에 뒤따라올 기나긴 겨울로부터 도망치기 위해 장벽을 넘으려 한다.''',
        '비세리스는 자신의 혈육을 누구와 결혼 시켰는가?',
        '칼 드로고',
        '칼 드로고'
        ),
    13:(
        '''이센스의 커리어에서 빼놓을 수 없는 작업물은 바로 믹스테잎인데 2007년에 힙합플레이야를 통해 첫 믹스테잎 <Blanky Munn's Unknown Verses>을 무료배포하였다. 특히 사이먼 도미닉과 마이노스가 참여한 'I'm No Good'이 대표적인 트랙. 이후 2008년 두번째 믹스테잎인 <New Blood, Rapper Vol.1>을 발표하는데 이 믹스테잎은 지금까지도 많은 사람들에게 웰메이드 믹스테잎이라 불리며, 국내힙합 믹스테잎하면 빠지지 않고 언급되는 대표적인 믹스테잎이 되었다. 이후 나오는 많은 래퍼들에게도 영향을 미쳤는데 대표적으로 블락비의 지코가 고등학교 시절 이 믹스테잎과 버벌진트의 노래를 듣고 본격적으로 랩을 시작하게 되었다고 한다. 2007년 사이먼 도미닉과 슈프림팀을 결성하였고, 정식 작업물 없이도 최고의 시너지를 내는 언더그라운드 듀오의 면모를 뽐내기도 하였다. 이후 다이나믹 듀오의 소속사인 아메바컬쳐에 들어가게 된다. 언더그라운드씬을 씹어먹고 다니던 최고의 슈퍼루키가 팀으로 뭉쳤다 보니 사람들의 많은 기대를 모았다.''',
        '고등학생 때 이센스와 버벌진트로부터 영향을 받은 래퍼는?',
        '지코',
        '지코'
        ),
    14:(
        '''롯데리아의 경우, 타 브랜드에 비해 햄버거 조리 후의 홀딩 시간이 길어서 소비자에게 가는 햄버거가 최상의 맛이 아닌 경우가 많다. 일단 매뉴얼 상에는 재료 별로 홀딩 시간이 정해져 있고 완제품 버거의 홀딩 시간도 따로 규정이 있다. 직영점은 이 홀딩 시간을 지키지만 가맹점은 정말 멋대로라 최악의 햄버거를 맛보는 일도 왕왕 발생한다. 맥도날드의 경우, 패티를 미리 구워 홀딩해두지만 완제품 버거는 홀딩이 없고 주문이 들어올 때마다 조리한다. 맥도날드는 패티 종류가 7가지 밖에 안 되어서 조리 후 비교적 빠른 시간 안에 소비되기 때문에 비교적 좋은 상태로 제품이 나갈 확률이 높다. 버거킹은 완제품 홀딩이 있기는 하지만 홀딩 시간이 10분으로 롯데리아보다 훨씬 짧고, 소비자가 요청할 시 새로 조리를 해준다. 홀딩을 한다 해도 대부분 행사 제품을 홀딩하는 경우가 절대 다수.''',
        '맥도날드에서는 몇가지 패티를 사용하는가?',
        '7가지',
        '7가지'
        ),
    15:(
        '''호그와트 마법학교 4학년이 된 해리 포터는 여름방학 동안 위즐리 가족과 함께 퀴디치 월드컵을 관람한다. 경기가 끝난 후 축제 분위기로 들뜬 텐트촌에, 갑자기 볼드모트를 숭배하는 죽음을 먹는 자들이 나타나 테러가 벌어진다. 주위를 온통 광란의 도가니로 몰아넣음과 동시에, 하늘에는 볼드모트의 상징인 '어둠의 표식'이 나타난다. 개학이 되어 다시 호그와트로 돌아간 해리 포터는 알버스 덤블도어 교장으로부터 "올해에는 퀴디치 게임 대신 트리위저드 시합을 개최하게 되었다"는 뜻밖의 소식을 듣는다. 보바통과 덤스트랭 그리고 호그와트의 챔피언들이 1명씩 참가하는 트리위저드 시합의 우승자는 1천 갈레온의 상금과 최고의 영예를 얻게 된다. 그러나 17세 이상의 학생만이 이 시합에 참가할 수 있었기 때문에, 해리는 자신의 이름을 불의 잔에 넣을 수 없다. 해리는 어둠의 마법방어술을 가르치기 위해 새로 부임한 매드아이 무디 교수와 돈독한 우의를 다지게 된다. ''',
        '트리위저드 시합은 몇 살부터 나갈 수 있는가?',
        '17세',
        '17세'
        ),
    16:(
        '''U-GO-GIRL은 연간 음원순위 8위, 각종 음악방송 트리플 크라운에 올랐으며 OK춤도 상당한 인기를 끌었다. 'Hey Mr. Big' 역시 연간 음원순위 20위에 오를 정도로 흥행했으며, 후속곡으로는 솔로 활동 이후 처음으로 음악방송에서 2주 연속 1위를 차지한다. 음반판매량 역시 한터차트로는 5만 5천장으로 전작을 약간 상화하는 판매고를 올렸고, 음협으로도 7만 5천장을 기록하면서 음악적으로 큰 성과를 냈는데, 무게감을 덜어내고 대중친화적인 스타일을 선택했다는 점이 호응을 이끌어 낸 것으로 평가된다. 특히 그동안 끊임없이 제기되던 가창력 논란과 평론가들의 혹평을 완전히 반전시키며, 전체적으로 온전히 가수로서 평가 받는 계기가 된 음반이다. 2008년. 패밀리가 떴다에 출연해 유재석과 국민남매 기믹을 맡아 활약했다. 또 주인님 효리와 펫 종국을 포함한 여러 라인을 선보이며 활약, 시청률 30%를 웃도는 높은 인기를 구가한다. 이듬해 유재석과 함께 SBS 예능 대상을 수상했다.''',
        '이효리와 함께 대상을 탄 사람은 누구인가?',
        '유재석',
        '유재석'
        ),
    17:(
        '''2017년 3월 26일 <런닝맨> 방송이 나왔으며, 여기서 소소한 활약을 했다. 유재석과 같은 팀이 되었는데 유재석과는 지난 무한도전 캘리포니아 L.A.에서 롤러코스터를 같이 탄 이후 두 번째로 같은 팀이 되었다. 첫 번째 노래방 대결에서는 댄스를 유감없이 선보였으며, 마지막 노래부르기에서는 <오늘부터 우리는> 을 혼자서 완벽하게 불러내며 98점이라는 높은 점수를 받아냈다. 두 번째 역사 퀴즈 대결에서는 일부러 어려운 영어 문제를 출제하여 상대에게 시간을 소비하게 했으며, 본인은 상대가 낸 어려운 문제를 쉽게 찾아내면서 정답을 맞추기도 했다. 이후 지갑바꾸기 찬스에서는 유재석이 이광수에게서 가져온 지갑을 다시 이광수에게 빼앗기기 직전에 그 지갑에서 돈을 빼내는 영리한 플레이를 했으며, 마지막 미션에서는 김종국이 숨겨놓은 돈을 그 날 출연진 중 유일하게 찾아내기도 했었다. 여자친구 내에서도 브레인으로 통하는 만큼 그야말로 게임 내에서도 브레인의 모습을 유감없이 보여줬다.''',
        '여자친구 안에서 유주의 별명은 무엇인가?',
        '브레인',
        '브레인'
        ),
    18:(
        '''LG CNS가 스마트시티 사업에 승부수를 띄운다. 김영섭 LG CNS 대표가 직접 선진모델 학습과 글로벌 기업과 협력을 챙기며 공을 들인다. 22일 LG CNS에 따르면 김영섭 대표는 내달 13일 스페인 바르셀로나에서 열리는 '스마트시티 월드 콩그레스(Smart City World Congress) 2018'에 참가한다. 행사는 스마트시티 관련 국제 최대 콘퍼런스이자 전시회다. 김 대표는 사흘간 열리는 행사에 참석, 스마트시티 관련 글로벌 표준과 정책을 공유하고 협업을 모색한다. 스마트시티 글로벌 표준 논의에 참여하고 세계 정보기술(IT)기업과 협력도 추진한다. 스마트시티 관련 올해만 벌써 네 번째 출장이다.  LG CNS는 자사 사물인터넷(IoT) 플랫폼 '인피오티'와 스마트시티 플랫폼 시티허브를 중심으로 스마트시티 사업을 펼친다. 김 대표가 참가한 해외 콘퍼런스는 물론 싱가포르 스마트네이션과 소프트웨이브·IoT국제전시회 등에 참여해 트렌드를 확인하고 스마트시티 플랫폼을 알렸다.''',
        'LG CNS의 스마트시티 사업의 주축이 되는 플랫폼들중 IoT와 관련있는 것은?',
        '인피오티',
        '인피오티'
        ),
    19:(
        '''9일 출시된 ERP상품 ‘LG CNS EAP’가 이번 도전의 주인공이다. 고객이 시스템을 사용하면 과거에 2시간 이상 걸리던 수백만건의 정보처리 업무를 10분만에 마칠 수 있다고 LG CNS측은 설명하고 있다. 대화 형식으로 경영업무를 도와주는 인공지능로봇(챗봇) 기술이 적용된 덕분이다. 경영업무 중 가장 복잡하고 난이도가 있어 자동화가 쉽지 않았던 급여계산 작업에도 EAP를 사용하면 소요 시간이 절반 가량으로 줄어든다고 LG CNS측은 소개했다. 영업 분야에선 소프트웨어 로봇 프로세스 자동화 기술인 RPA(Robotic Process Automation)가 작동돼 단순 업무를 자동화시킬 수 있다. 해당 시스템 이용시 고객은 업무처리 속도를 최대 80% 높일 수 있다고 이 회사 관계자들은 자신했다.''',
        '로봇 프로세스 자동화 기술을 사용하면 업무처리 효율이 얼마나 개선되는가?',
        '80%',
        '80%'
        ),
    20:(
        '''해방 직후 북에서 월남한 실향민들이 집단으로 거주하면서 이 지역에 촌락을 이루게 되고, 이후 도시가 발전하며 이촌향도한 이주민들이 다시 한번 대거 들어와 동네를 형성하게 된다. 서울의 대표적인 달동네 중 한곳이라 한때는 서울시에서 이곳을 녹지화한다는 계획도 있었지만 반발이 심해 무산된 바 있다. 그러다가 2000년대 중후반부터 인근 이태원동이 사람들의 주목을 받고 뜨는 동네가 되면서 인근의 해방촌에도 유동인구가 몰리기 시작했다. 특히 이곳에 있던 외국인들을 위한 소규모 식당들이 맛집으로 인기를 얻으면서 상권이 점차 확대되었고, 현재는 젠트리피케이션으로 인해 원주민들은 다른 동네로 밀려났으나, 다시 사람들이 붐비고 있다. 옆동네 경리단길과 비슷하게 주말에는 힙스터와 맛집애호가들로 시끌벅적하다. 하지만 입소문으로 인기를 얻은 동네가 으레 그렇듯 이 지역 주민들은 인기 맛집보다는 저렴한 동네가게를 들리는 경우가 많다.''',
        '해방촌 주민들이 다른 곳으로 밀려나게 된 계기는 무엇인가?',
        '젠트리피케이션',
        '젠트리피케이션'
        ),
    21:(
        '''1945년 8.15 광복을 맞고 분단 체제가 성립되면서 남한의 평양냉면 문화는 북한과 완전히 단절되었다. 특히 1950년 6.25 전쟁은 남한의 평양냉면이 원형과는 완전히 다른 음식으로 바뀌는 데 결정적인 역할을 하였다. 왜냐하면 전쟁으로 대규모의 함경도 피난민들이 서울에 유입되었기 때문이다. 전쟁으로 함경도에서 내려온 실향민들은 살아남기 위해 요식업계에 뛰어들기 시작했는데, 그들이 고향에서 먹던 해산물 및 감자, 호밀, 귀리 등등은 서울에서 구하기 매우 힘들었다. 따라서 함경도 사람들은 자신들이 먹던 고향의 음식을 내세우기는커녕 아예 만들어 먹을 수조차 없는 형편이었다. 그런데 그나마 쉽게 재료를 구할 수 있는 것은 감자전분으로 만든 농마국수였다. 그들이 부르는 국수의 이름은 서울에서는 너무나 생소했기 때문에, 서울에서 이미 널리 알려진 이름을 차용해 '함흥냉면'이라는 브랜드를 만들었다. 이로 인해 평양냉면에는 함경도의 국수 문화가 크게 섞이면서 원형과는 완전히 다른 형태로 분화하기 시작했다.''',
        '함흥냉면이 유래한 음식은?',
        '농마국수',
        '농마국수'
        ),
    22:(
        '''빼빼로의 길쭉길쭉한 생김새를 아라비아 숫자 '11'에 끼워맞춰 퍼뜨린 것이 오늘날에 이르고 있다. 시초는 1993년의 부산광역시 황령산 아래 어느 여고에서 시작되었다. 지금은 폐교된 계성여중이 시초라는 설도 있다. 경남지역 소장이 매년 11월 11일만 되면 빼빼로가 엄청나게 팔린다며 본사에 제보를 했고, 조사해보니 그 지역 여학생들끼리 다이어트에 성공해 빼빼하게 되자, "살 좀 빼라"고 놀리며 빼빼로를 나눠먹는 날이었다고 한다. 이를 본사에서 발빠르게 마케팅에 사용하며 전국적으로 퍼져 지금에 이르게 된 것. 언론에서는 1996년 11월부터 차츰 다뤄지기 시작했으며 2000년대 들어서 상당한 규모로 커져서 현재는 1년 판매량의 5~60% 가량이 빼빼로데이 전후로 나간다고 한다. 한국에서 시작한 마케팅 기념일이지만 일본에서도 뒤늦게 이를 따라 '포키 데이' 라는 것을 만들어 홍보중이다.''',
        '빼빼로 데이가 시작된 도시는?',
        '부산광역시',
        '부산광역시 황령산'
        ),
    23:(
        '''일본 제1의 도시답게 도쿄도 기준 인구는 1,300만 명이 넘는다. 보통은 도쿄 23구만 도쿄로 보는 경우가 많은데 23구 기준으로만 하면 인구는 937만명 정도이다. 때문에 보통 도쿄의 인구는 900여만명 정도로 표기된다. 그럼에도 이는 대단한 인구수로 단일 행정구역으로 이 정도의 인구가 몰려사는 도시는 전 세계를 통틀어도 서울 등 소수이긴 하다. 도쿄 23구만 놓고보면 인구는 2016년 10월 기준으로 약 937만 명이고 면적은 619 km²로 서울이랑 비교하면 인구는 대략 50여만 명이 적고 면적은 고작 14 km² 더 넓다. 도쿄와 주변을 전부 포함하는 수도권의 인구는 대략 4,330만 쯤 된다. 면적 또한 매우 넓은 2,187 km²로(서울의 3배) 일종의 메갈로폴리스이기 때문에 거주 인구밀도 자체는 서울보다 높지 않다. 도쿄의 알짜배기라고 할 수 있는 도쿄 23구의 인구밀도는 1 km²당 14,727명으로 서울과 비슷하다.''',
        '도쿄의 알짜배기 지역의 인구는 얼마인가?',
        '937만명',
        '937만명'
        ),
    24:(
        '''감독 경력에 관심을 보인, 애플렉은 존 프랑켄하이머 감독의 액션 스릴러 《레인디어 게임》의 사전 제작에 그림자처럼 따라 다녔다. 프랑켄하이머는 애플렉에 자신의 마지막 장편 영화가 될 것이라고 설명하며, 그에 대해 “매우 마음을 이끄는, 좋은 자질을 갖추고 있다. 나는 오랫동안 이 일을 했지만 그는 정말 멋진 사람 중 하나이다.”라고 칭찬했다. 그는 샤를리즈 테론의 상대역으로 출연했다. 그는 범죄 드라마 《보일러 룸》(2000)에서 조연 역할의 인정사정 없는 증권 중개인으로 출연했다. 2000년 그의 마지막 역할로, 애플렉은 로맨틱 드라마 《바운스》에서 그의 여자친구 귀네스 팰트로의 상대역을 연기했다. 2000년에는 또한, 그는 애니메이션 《이집트 왕자 2:요셉이야기》에서 요셉의 목소리를 연기했다.''',
        '《레인디어 게임》에서 애플렉의 상대역의 이름은 무엇인가?',
        '샤를리즈 테론',
        '샤를리즈 테론'
        ),
    25:(
        '''조선 왕조 동안 저고리는 점차 짧아지면서 그 부피도 펑퍼짐했던 것에 비해 좀 더 몸에 달라 붙는 형태로 바뀌게 됐다. 16세기 이전에 저고리는 현재의 배기팬츠처럼 펑퍼짐해 허리 밑으로 쳐질 정도였지만 임진왜란 이후 피폐해진 국가 상황으로 천을 덜 쓰는 쪽으로 의복이 변화되게 되었다. 18세기가 지나면서 짧고 상반신으로 더 올라온 저고리는 거의 가슴을 덮지 않는 정도로 짧아져 여성들은 허리띠를 높이 착용해야 했다. 원래는 치마를 동여매는 용도로 드러내지 않았으나 허리띠는 18세기 후반에 들어 패션 소품으로서 드러내게 되어 19세기에는 보편화 되었다. 그러나 중인과 천민은 아들을 낳았을 경우에만 허리띠를 노출했으므로 거의 허리띠를 드러내 매고 다니지 않았다.''',
        '가슴을 덮기 위해 조선 여성들이 사용한 것은?',
        '허리띠',
        '허리띠'
        ),
    26:(
        '''결국 〈좋은 날〉은 음반 발매 일주일여만에 공중파 음악 프로그램인 SBS 《인기가요》에서 단독으로는 처음으로 1위를 차지했고, 이어서 3주 연속으로 1위를 차지해 트리플 크라운을 달성했다. 또한 KBS 《뮤직뱅크》 K차트에서 3주 연속 1위, Mnet 《엠 카운트다운》에서도 1위를 차지하며 지상파, 케이블 방송의 음악 순위 프로그램에서 모두 1위를 하는 성과를 얻었다. 온라인 음원사이트에서도 많은 인기를 얻었는데, 멜론에서는 2010년 12월 10일에서 2011년 1월 7일까지 일간차트에서 연속 29일 동안 1위를 하는 기염을 토하였고, 2010년 12월의 월간차트도 멜론, 도시락, 엠넷, 소리바다 등 월간차트를 제공하는 모든 음원사이트에서 1위를 차지했다.''',
        '아이유의 좋은 날은 멜론의 일간차트에서 며칠간 연속 1위를 하였는가?',
        '29일',
        '29일'
        ),
    27:(
        '''처음에는 동구릉이 있는 구리시에서 왕릉 관광지 개발을 위해 2003년에 동구릉의 등재를 추진하다가 2004년에 문화재청이 조선왕릉 40기에 대한 일괄 등재를 추진하기로 결정하였다. 2008년 1월에 유네스코 세계유산위원회에 신청서를 제출하였고, 그 해 9월에 ICOMOS(국제기념물유적협의회)의 현지 조사가 이뤄졌고, 2009년 1월에 ICOMOS는 일부 조선왕릉 주변지대의 분류와 주변 시설에 대한 철거에 대한 문제 해결을 문화재청과 한국정부에 요청하였고, 이에 대한 답변을 확인하고서 그 해 5월에 ‘등재 권고’가 적힌 평가보고서를 유네스코에 제출하였다. 그리고 2009년 6월 27일, 유네스코는 스페인 세비야에서 열린 제33차 세계유산위원회에서 조선왕릉 40기를 세계유산으로 등재하였다.''',
        '2004년에 조선왕릉 40기에 대한 세계유산 등재를 추진하기로 결정한 기관은?',
        '문화재청',
        '문화재청'
        ),
    28:(
        '''2008년 11월 30일 서태지는 《SBS 인기가요》 프로그램에 출연하여 본격적인 공중파 활동을 시작했다. 이후 서태지는 12월 6일에 MBC에서 방영하는 《쇼 음악중심》, SBS에서 방영하는 《인기가요》에 출연하였다. 여기서 서태지는 "Human Dream"의 ‘쫄핑크 댄스’를 통해 서태지와 아이들 4집 이후 10여 년 만에 댄스가수로서의 면모를 다시 선보였다. "Human Dream"의 뮤직비디오는 12월 12일 방송된 MBC 에브리원 《신해철의 스페셜 에디션》 1회에 처음 공개되었다. 이 뮤직비디오는 블록버스터급의 뮤직비디오로 부산 벡스코 앞에서 대규모 폭발 장면을 촬영한 것으로 알려졌었다. 이후 파이널 에피소드는 곰TV를 통해 공개됐다. 현재까지 서태지의 8집 첫 번째 싱글 앨범은 20만 장 이상의 판매량을 기록하였다.''',
        'Human Dream의 파이널 에피소드는 어디에서 공개되었는가?',
        '곰TV',
        '곰TV'
        ),
    29:(
        '''야민정음에 관해 종종 "세종대왕이 무덤에서 보면 어떻겠냐"라는 논리의 부정여론이 형성되지만, 사실상 세종대왕은 한글을 만든 것이지 국어를 만든 것이 아니다. 한글을 통한 단어들은 시대에 따라 바뀔 수 있는 것이고, 오히려 세종대왕은 아직도 한글이 쓰이고 있는 것에 대해 만족할 수도 있다. 덧붙여서 글자 모습의 유사성을 가지고 다르게 표현하는 행위는 애초에 훈민정음에서 기존 한자의 모습을 토대로 설명하는 과정에서 사용되었기 때문에, 우스갯소리로 세종대왕이야말로 야민정음의 창시자가 아니냐는 말도 있다.''',
        '세종대왕이 사실상으로 만든 것은 무어라고 봐야 옳을까?',
        '한글',
        '한글'
        ),
    30:(
        '''울지 마라. 수선화 외로우니까 사람이다. 살아간다는 것은 외로움을 견디는 일이다. 공연히 오지 않는 전화를 기다리지 마라. 눈이 오면 눈길을 걸어가고 비가 오면 빗길을 걸어가라. 갈대 숲에서 가슴검은도요새도 너를 보고 있다. 가끔은 하느님도 외로워서 눈물을 흘리신다. 새들이 나뭇가지에 앉아 있는 것도 외로움 때문이고 네가 물가에 앉아 있는 것도 외로움 때문이다. 산 그림자도 외로워서 하루에 한 번씩 마을로 내려온다. 종소리도 외로워서 울려 퍼진다.''',
        '갈대 숲에서 너를 보고 있는건 누굴까',
        '가슴검은도요새',
        '가슴검은도요새'
        ),
    31:(
        '''벨레로폰은 헤라클레스 이전의 가장 위대한 영웅으로 카드모스와 페르세우스와 어깨를 나란히 하였다. "벨레로폰테스"라고도 하며 뜻은 '벨레로스(Belelos)를 죽인 자'이다. 죄를 짓고 아르고스의 왕에게 피tls하여 있던 그는 왕비 안테이아가 자신에게 반하자 거절하였다. 왕비는 분한 마음에 남편 프로이토스에게 거짓으로 벨레로폰이 자기를 농락하려 한다고 고하였다. 아르고스의 왕은 벨레로폰을 직접 죽이기 싫어서 편지 한 장을 뤼키아왕인 이오바테스(Iobates)에게 보낸다. 이 편지의 내용은 이 편지를 갖고 오는 자를 죽여 달라는 것이었다. 이처럼 '자신에게 지극히 불리한 편의 편지'를 '벨레로폰의 편지(Bellerophonic letter)'라 한다.''',
        '벨레로폰은 누구를 죽였는가?',
        '벨레로스',
        '벨레로스'
        ),
    32:(
        '''텅 비어 있는 것을 경험해 봐야 가득 찬 것의 가치를 알게 되죠. 수도사들은 말하는 것의 기쁨을 알기 위해 침묵 수행을 하고, 음식의 참맛을 알기 위해 금식을 합니다. 또한 정적을 알아야 음악을 제대로 즐기게 되고, 어둠을 경험해야 색깔의 참된 가치를 이해하게 되죠''',
        '음식의 참맛을 이해하기 위해선 무엇을 해야 할까?',
        '금식',
        '금식'
        ),
    33:(
        '''다른 쪽을 돋보이게 할 목적으로 쓰이는 집단이 있는데, 이들을 보면 사람들은 무조건 <아니요>라고 말하고 싶은 마음이 든다. 왜냐하면 이 집단의 구성원들은 수단 방법을 가리지 않고 남의 반감을 자아내는 사람들이기 때문이다. 그들은 큰 소리로 마하고, 쉽게 남을 모욕하고, 거짓말도 맞는 말이라고 강변하며, 공격적이다. 그들은 음첨한 행동과 비양심적 행위를 기꺼이 도맡아서 한다. 그러므로 사람들은 본능적으로 이러한 허수아비 집단이 제안하는 것의 반대편에 표를 던진다. 무의식적으로 우리는 이런 위치에 서는 것이다. <이 주장은 그들에게서 나온 것이니까, 반대해야 해.> 그들은 <역(逆) 프로그래머>처럼 행동한다.''',
        '일부러 반감을 자아내서 반대편에 표를 던지도록 하는 목적의 집단은?',
        '허수아비 집단',
        '허수아비 집단'
        ),
    34:(
        '''"최초로 물 밖으로 나와 육지로 기어 올라온 물고기의 심정이 어땠겠어요? 물 밖으로 나오기 무섭게 다시 물속으로 돌아가고 싶었을 거에요. 사실 다시 물로 돌아간 물고기들도 많고요."
"소수의 물고기들만이 그 당황스러운 서식 환경에 적응했지."
"어떤 물고기들이 말인가요?"
"불만에 찬 물고기들 말이오. 물속에서 사는 게 편치 않았던 물고기들. 편안함을 느낀다면 삶을 변화시키고 싶은 마음이 생길 이유가 전혀 없겠지. 고통만이 우리를 일깨우고, 문제의식을 가지고 모든 것을 대하게 만들지요."
"나는 우리가 고통 없이도 진화할 수 있다고 믿어요."
"나도 그랬으면 좋겠소. 하지만 인류의 역사를 돌이켜보면 진보는 항상 고통 속에서만 가능했소... 일종의 습성인 셈이지."''',
        '인류의 진보는 무엇을 계기로 가능하였나?',
        '고통',
        '고통 속'
        )

}

# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')


class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')
    radio_field = RadioField('This is a radio field', choices=[
        ('head_radio', 'Head radio'),
        ('radio_76fm', "Radio '76 FM"),
        ('lips_106', 'Lips 106'),
        ('wctr', 'WCTR'),
    ])
    checkbox_field = BooleanField('This is a checkbox',
                                  description='Checkboxes can be tricky.')

    # subforms
    mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    office_phone = FormField(TelephoneForm, label='Your office phone')

    ff = FileField('Sample upload')

    submit_button = SubmitField('Submit Form')


    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        return render_template('index.html', form=form)

    return app

def create_app_new(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)
    flask_sijax.Sijax(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    @app.route('/', methods=('GET', 'POST'))
    def index():
        form = ExampleForm()
        form.validate_on_submit()  # to get error messages to the browser
        flash('critical message', 'critical')
        flash('error message', 'error')
        flash('warning message', 'warning')
        flash('info message', 'info')
        flash('debug message', 'debug')
        flash('different message', 'different')
        flash('uncategorized message')
        return render_template('index.html', form=form)

    @app.route('/congrats')
    def congrats():
        return render_template('congrats.html')

    @app.route('/wrong')
    def wrong():
        return render_template('wrong.html')


    @app.route('/quiz')
    def quiz():
        qid = random.sample(range(len(qa_set.keys())), 1)[0]
        contents, question, answer, score = qa_set[qid]

        correct_count = 0
        if request.args.get('correct_count'):
            correct_count = int(request.args.get('correct_count'))

        ai_correct_count = 0
        if request.args.get('ai_correct_count'):
            ai_correct_count = int(request.args.get('ai_correct_count'))

        correct_qids = []
        if correct_count > 0:
            if request.args.get('correct_qids'):
                correct_qids = request.args.get('correct_qids').split(',')
                print(correct_qids)
                while (str(qid) in correct_qids):
                    qid = random.sample(range(len(qa_set.keys())), 1)[0]

        # for key in request.args.keys():
        #     print(key + '  ' + request.args.get(key))
        #     print(int(request.args.get('ai_correct_count')))
        #     print


        return render_template('quiz.html', contents=contents, qid=qid, question=question, correct_count=correct_count, ai_correct_count=ai_correct_count, correct_qids=','.join(correct_qids))

    # @flask_sijax.route(app, '/result')
    @app.route('/result', methods=['POST'])
    def result():
        # Every Sijax handler function (like this one) receives at least
        # one parameter automatically, much like Python passes `self`
        # to object methods.
        # The `obj_response` parameter is the function's way of talking
        # back to the browser
        # def say_hi(obj_response):
        #     obj_response.alert('Hi there!')


        correct_count = int(request.form['correct_count'])
        ai_correct_count = int(request.form['ai_correct_count'])
        correct_qids = request.form['correct_qids'].split(',')

        #ai_correct_count = int(request.form['ai_correct_count'])
        
        qid = request.form['qid']

        answer = request.form['answer']
        ai_answer = qa_set[int(qid)][3]
        correct_answer = qa_set[int(qid)][2]

        result_message = ''
        animation = ''
        ai_result = ''
        human_result = ''



        if ai_answer == correct_answer:
            ai_result = 'correct'
            ai_correct_count = ai_correct_count + 1
        else:
            ai_result = 'wrong'

        if correct_answer == answer:
            result_message = '정답이에요~';
            animation = 'pulse slow';
            human_result = 'correct'
            correct_count = correct_count + 1
            if correct_qids == ['']:
                correct_qids = [qid]
            else:
                correct_qids.append(qid)

        else:
            result_message = '땡! 기계보다 못한..'
            animation = 'hinge delay-2s'
            human_result = 'wrong'
            correct_qids = []

        result = str(correct_answer==answer)
        
        
        # if g.sijax.is_sijax_request:
        #     # Sijax request detected - let Sijax handle it
        #     g.sijax.register_callback('say_hi', say_hi)
        #     return g.sijax.process_request()

        # Regular (non-Sijax request) - render the page template
        return render_template('result.html', 
            result_message=result_message,
            correct_answer=correct_answer,
            animation=animation,
            ai_result=ai_result,
            human_result=human_result,
            answer=answer,
            correct_count=correct_count,
            ai_correct_count=ai_correct_count,
            result=(correct_answer==answer),
            ai_answer=ai_answer,
            correct_qids=','.join(correct_qids))
        #return json.dumps({'result_message':result_message,'correct_answer':correct_answer,'animation':animation});


    return app

if __name__ == '__main__':
    create_app_new().run(debug=True)
