<template>
    <div class="container">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Регистрация</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>ИИН</label>
                        <div class="control">
                            <input type="text" name="username" class="input" v-model="username" placeholder="Введите иин"
                                   pattern="\d{12}" title="ИИН должен состоять из 12 цифр">
                        </div>
                    </div>
                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" name="password1" class="input" v-model="password1" placeholder="Введите пароль">
                        </div>
                    </div>
                    <div class="field">
                        <label>Повторите пароль</label>
                        <div class="control">
                            <input type="password" name="password2" class="input" v-model="password2" placeholder="Повторите пароль">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Подтвердить</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'

    import {toast} from 'bulma-toast'

    export default {
        name: 'SignUp',
        data() {
            return {
                username: '',
                password1: '',
                password2: '',
                errors: []
            }
        },
        methods: {
            async submitForm() {
                this.errors = []
                if (this.username === '') {
                    this.errors.push('Добавьте ИИН')
                }
                if (this.password1 === '') {
                    this.errors.push('Пароль короткий')
                }
                if (this.password1 !== this.password2) {
                    this.errors.push('Пароли не совпадают')
                }
                if (!this.errors.length) {
                    this.$store.commit('setIsLoading', true)

                    const formData = {
                        username: this.username,
                        password: this.password1,
                    }
                    await axios
                        .post('/api/v1/users/', formData)
                        .then(response => {
                            toast({
                                message: 'Account was created, please log in',
                                type: 'is-success',
                                dismissible: true,
                                pauseOnHover: true,
                                duration: 2000,
                                position: 'bottom-right',
                            })
                            this.$router.push('/log-in')
                        })
                        .catch(error => {
                            if (error.response) {
                                for (const property in error.response.data) {
                                    this.errors.push(`${property}: ${error.response.data[property]}`)
                                }
                            } else if (error.message) {
                                this.errors.push('Something went wrong. Please try again!')
                            }
                        })
                    this.$store.commit('setIsLoading', false)
                }
            }
        }
    }
</script>