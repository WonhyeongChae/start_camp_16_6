export const travelTypes = [
  { code: 'HEALING', name: '고요한 쉼표 수집가', description: '자연 속에서 재충전하는 느긋한 여행자', icon: '🌿', tone: 'green' },
  { code: 'EXPLORER', name: '에너지 만렙 탐험가', description: '짜릿한 액티비티와 도전을 즐기는 모험가', icon: '🥾', tone: 'blue' },
  { code: 'CULTURE', name: '이야기를 좇는 시간여행자', description: '역사와 문화 속에서 의미를 찾는 여행자', icon: '🏯', tone: 'purple' },
  { code: 'FOODIE', name: '한입에 담는 로컬 미식가', description: '시장의 맛과 로컬 식문화를 사랑하는 미식가', icon: '🍲', tone: 'orange' }
]

export const places = [
  {
    contentId: '3566301', shortTitle: '금오산', title: '금오산도립공원', category: '자연',
    description: '호수와 케이블카, 멋진 전망으로 힐링 가득한 시간',
    imageUrl: 'https://tong.visitkorea.or.kr/cms/resource/01/3566301_image2_1.jpg', matchedKeywords: ['자연', '휴식', '산책']
  },
  {
    contentId: '4063260', shortTitle: '금오서원', title: '금오서원', category: '역사·문화',
    description: '조선시대 유학자의 숨결이 살아있는 고즈넉한 공간',
    imageUrl: 'https://tong.visitkorea.or.kr/cms/resource/60/4063260_image2_1.jpg', matchedKeywords: ['역사', '문화']
  },
  {
    contentId: '3032819', shortTitle: '검성지 생태공원', title: '검성지 생태공원', category: '자연',
    description: '고요한 호수와 산책로가 어우러진 평화로운 자연 쉼터',
    imageUrl: 'https://tong.visitkorea.or.kr/cms/resource/08/3032808_image2_1.jpg', matchedKeywords: ['자연', '산책', '조용함']
  }
]

export const festivals = [
  { id: 1, schedule: '일정 확인 중', title: '구미라면 축제', description: '라면과 함께하는 맛있고 재미있는 구미의 대표 축제!', location: '구미시 낙동강체육공원' },
  { id: 2, schedule: '일정 확인 중', title: '구미푸드페스티벌', description: '다양한 로컬 먹거리와 공연이 어우러지는 미식 축제!', location: '구미시 송정동 일원' }
]

export const posts = [
  { id: 1, category: '여행 후기', title: '금오산 케이블카 타고 힐링했어요!', views: '1,246', time: '2시간 전', tone: 'green' },
  { id: 2, category: '맛집 추천', title: '새마을시장 숨은 맛집 리스트', views: '893', time: '5시간 전', tone: 'blue' },
  { id: 3, category: '자유 이야기', title: '7월에 가볼 만한 구미 여행지는?', views: '652', time: '1일 전', tone: 'purple' }
]

export const heroImages = [
  { alt: '금오산의 푸른 풍경', src: 'https://tong.visitkorea.or.kr/cms/resource/01/3566301_image2_1.jpg' },
  { alt: '고즈넉한 금오서원', src: 'https://tong.visitkorea.or.kr/cms/resource/60/4063260_image2_1.jpg' },
  { alt: '검성지 생태공원', src: 'https://tong.visitkorea.or.kr/cms/resource/08/3032808_image2_1.jpg' }
]
