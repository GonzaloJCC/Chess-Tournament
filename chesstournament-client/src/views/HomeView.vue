<template>
    <div class="wrap-all-three">
        <template v-if="isLoggedIn">
            <HomeInfoAdmin />
        </template>
        <template v-else>
            <HomeInfo />
        </template>
        <div class="bottom-row">
            <HomeTournaments />
            <HomeSearch />
        </div>
    </div>
</template>

<script setup>
import HomeInfo from '@/components/HomeInfo.vue';
import HomeInfoAdmin from '@/components/HomeInfoAdmin.vue';
import HomeTournaments from '@/components/HomeTournaments.vue';
import HomeSearch from '@/components/HomeSearch.vue';
import { useTokenStore } from '@/stores/token';
import { computed } from 'vue';

// Accede al tokenStore
const tokenStore = useTokenStore();

// Computed para verificar si el usuario está logueado
const isLoggedIn = computed(() => tokenStore.token !== null);
</script>

<style scoped>
html {
    font-size: 16px;
}

.wrap-all-three {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    padding: 2rem;
    width: 100%;
}

.bottom-row {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    flex-grow: 1;
    justify-content: center;
    width: 100%;
}

.home-info, .home-tournaments, .home-search {
    padding: 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 100%;
    max-width: 37.5rem;
    font-size: 1.25rem;
    font-family: 'Cascadia Code', Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 9.375rem;
}

.home-tournaments {
    background-color: rgba(4, 38, 243, 0.34);
}

.home-search {
    background-color: rgba(195, 22, 22, 0.34);
}

@media (max-width: 48rem) {
    .bottom-row {
        flex-direction: column;
        gap: 1.5rem;
    }

    .home-info, .home-tournaments, .home-search {
        width: 90%;
    }
}

@media (max-width: 30rem) {
    .home-info, .home-tournaments, .home-search {
        font-size: 1rem;
        padding: 1rem;
    }
}
</style>
