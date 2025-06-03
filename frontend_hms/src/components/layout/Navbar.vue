<template>
    <nav class="navbar">
        <div class="navbar-brand">
            <router-link to="/" class="navbar-item">
                <font-awesome-icon class="navbar-icon" icon="fa-solid fa-hospital" />
                <strong>Astana Hospital</strong>
            </router-link>
        </div>
        <div class="navbar-menu">
            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <template v-if="!$store.state.isAuthenticated">
                            <router-link to="/sign-up" class="button is-success">Регистрация</router-link>
                            <router-link to="/log-in" class="button is-light">Вход по ИИН</router-link>
                        </template>

                        <template v-else>
                            <router-link to="/dashboard/my-account" class="button is-info">
                                <font-awesome-icon icon="fa-solid fa-user" />
                                Мой профиль
                            </router-link>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    export default {
        name: 'Navbar',
        components: {FontAwesomeIcon}
    }
</script>

<style scoped>

.navbar {
    background-color: #2c3e50;
}

.navbar-icon {
    font-size: 40px;
}
</style>