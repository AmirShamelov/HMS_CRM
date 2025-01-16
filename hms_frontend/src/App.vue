<template>
    <div>
        <Navbar/>

        <section class="section">
            <RouterView/>
        </section>
    </div>

</template>

<script>
import Navbar from "@/components/layout/Navbar.vue"
import axios from "axios"

export default {
    name: 'App',
    components: {
        Navbar
    },
    beforeCreate() {
        this.$store.commit('initializeStore')

        if (this.$store.state.token) {
            axios.defaults.headers.common['Authorization'] = 'Token' + this.$store.state.token
        } else {
            axios.defaults.headers.common['Authorization'] = ''
        }
    },
}
</script>


<style lang="css">
@import "../node_modules/bulma";
</style>





