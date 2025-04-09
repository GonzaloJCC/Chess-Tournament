import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import CreateTournamentView from '@/views/CreateTournamentView.vue'
import TournamentDetailView from '@/views/TournamentDetailView.vue'
import FAQView from '@/views/FAQView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
	{
		path: '/log-in',
		name: 'login',
		component: LoginView
	},
	{
		path: '/log-out',
		name: 'logout',
		component: LogoutView
	},
	{
		path: '/createtournament',
		name: 'createtournament',
		component: CreateTournamentView
	},
	{
		path: '/tournamentdetail',
		name: 'tournamentdetail',
		component: TournamentDetailView
	},
	{
		path: '/tournamentdetail',
		name: 'tournamentdetail',
		component: TournamentDetailView
	},
	{
		path: '/faq',
		name: 'faq',
		component: FAQView
	}
  ]
})

export default router
