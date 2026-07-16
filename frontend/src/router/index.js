import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlacesView from '../views/PlacesView.vue'
import CommunityView from '../views/CommunityView.vue'
import CommunityWriteView from '../views/CommunityWriteView.vue'
import CommunityDetailView from '../views/CommunityDetailView.vue'
import TravelTestView from '../views/TravelTestView.vue'
import TravelResultView from '../views/TravelResultView.vue'
import FestivalsView from '../views/FestivalsView.vue'

// Leaflet은 지도 탭에 진입할 때만 내려받아 초기 화면 번들 크기를 줄입니다.
const MapView = () => import('../views/MapView.vue')

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/places', name: 'Places', component: PlacesView },
  { path: '/map', name: 'Map', component: MapView },
  { path: '/community', name: 'Community', component: CommunityView },
  { path: '/community/write', name: 'CommunityWrite', component: CommunityWriteView },
  { path: '/community/:id/edit', name: 'CommunityEdit', component: CommunityWriteView },
  { path: '/community/:id', name: 'CommunityDetail', component: CommunityDetailView },
  { path: '/travel-test', name: 'TravelTest', component: TravelTestView },
  { path: '/travel-result', name: 'TravelResult', component: TravelResultView },
  { path: '/festivals', name: 'Festivals', component: FestivalsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
