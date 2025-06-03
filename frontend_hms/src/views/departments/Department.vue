<template>
    <div class="department-container">
        <div class="department-card">
            <div class="department-header">
                <h1 class="department-title">{{ department.title }}</h1>
                <div class="title-decoration"></div>
            </div>

            <div class="department-content">
                <div class="description-wrapper">
                    <p class="department-description">{{ department.sub_title }}</p>
                </div>
            </div>

            <button @click="goToAppointment" class="appointment-btn">
                <span>Записаться на приём</span>
                <font-awesome-icon icon="fa-solid fa-arrow-right"/>
            </button>
        </div>

        <div class="doctors-section">
            <h2 class="doctors-title">Наши специалисты</h2>

            <div class="doctors-grid">
                <div v-for="doctor in filteredDoctors" :key="doctor.id" class="doctor-card">
                    <router-link :to="{ name: 'Doctor', params: {id: doctor.id}}">
                        <div class="doctor-photo-container">
                            <img :src="doctor.get_image" :alt="doctor.full_name" class="doctor-photo">
                        </div>
                    </router-link>
                    <div class="doctor-info">
                        <h3 class="doctor-name">{{ doctor.full_name }}</h3>
                        <p class="doctor-position">{{ doctor.position }}</p>
                        <button @click="openAppointmentModal(doctor)" class="doctor-appointment-btn">
                            Записаться
                            <font-awesome-icon icon="fa-solid fa-calendar-check"/>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="isModalOpen" class="modal-overlay">
            <div class="modal-content">
                <h3>Запись на прием к {{ selectedDoctor.full_name }}</h3>
                <form @submit.prevent="submitAppointmentForm">
                    <div class="field">
                        <label>Ваше имя</label>
                        <input type="text" v-model="appointmentForm.patient_name" required/>
                    </div>
                    <div class="field">
                        <label>Ваш ИИН</label>
                        <input type="text" v-model="appointmentForm.patient_iin" pattern="\d{12}"
                               title="ИИН должен состоять из 12 цифр" required/>
                    </div>
                    <div class="field">
                        <label>Дата приема</label>
                        <select v-model="appointmentForm.date" @change="loadAvailableTimes" required>
                            <option value="" selected>Выберите дату</option>
                            <option v-for="date in availableDates" :key="date" :value="date">
                                {{ date }}
                            </option>
                        </select>
                    </div>
                    <div class="field">
                        <label>Время приема</label>
                        <select v-model="appointmentForm.time" :disabled="!appointmentForm.date">
                            <option value="" selected>Выберите время</option>
                            <option v-for="time in availableTimes" :key="time.value" :value="time.value">
                                {{ time.label }}
                            </option>
                        </select>
                    </div>
                    <div class="field">
                        <label>Комментарий</label>
                        <textarea v-model="appointmentForm.comment"></textarea>
                    </div>
                    <div class="modal-buttons">
                        <button type="submit" class="button is-success">Отправить</button>
                        <button type="button" @click="closeAppointmentModal" class="cancel-button">
                            Отмена
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Department",
    data() {
        return {
            department: {},
            doctors: [],
            filteredDoctors: [],
            isModalOpen: false,
            selectedDoctor: null,
            appointmentForm: {
                patient_name: '',
                patient_iin: '',
                date: '',
                time: 1,
                comment: '',
            },
            availableTimes: [],
            availableDates: [],
        }
    },
    mounted() {
        this.getDepartment()
        this.getDoctors()
    },
    methods: {
        async getDepartment() {
            this.$store.commit('setIsLoading', true)

            const DepartmentID = this.$route.params.id

            await axios
                .get(`/api/v1/departments/${DepartmentID}/`)
                .then(response => {
                    this.department = response.data
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },
        async getDoctors() {
            this.$store.commit('setIsLoading', true)

            const DepartmentID = Number(this.$route.params.id)

            await axios
                .get('/api/v1/doctors/')
                .then(response => {
                    this.doctors = response.data.results
                    this.filteredDoctors = this.doctors.filter(doctor => {
                        return doctor.department.id === DepartmentID
                    })

                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },

        goToAppointment() {
            this.$router.push({name: "Doctors"})
        },
        openAppointmentModal(doctor) {
            this.selectedDoctor = doctor;
            this.isModalOpen = true;
            this.loadAvailableDates()
        },
        closeAppointmentModal() {
            this.isModalOpen = false;
            this.selectedDoctor = null;
            this.resetAppointmentForm();
        },
        resetAppointmentForm() {
            this.appointmentForm = {
                patient_name: '',
                patient_iin: '',
                date: '',
                time: 1,
                comment: '',
            };
            this.availableTimes = [];
            this.availableDates = [];
        },
        async loadAvailableDates() {
            this.$store.commit('setIsLoading', true)

            if (this.selectedDoctor) {
                await axios
                    .get(`/api/v1/appointments/available_dates/?doctor_id=${this.selectedDoctor.id}`)
                    .then(response => {
                        this.availableDates = response.data
                    })
                    .catch(error => {
                        console.log(error)
                        this.availableDates = [];
                    })
            }
            this.$store.commit('setIsLoading', false)
        },
        async loadAvailableTimes() {
            this.$store.commit('setIsLoading', true)

            if (this.selectedDoctor && this.appointmentForm.date) {
                await axios
                    .get(`/api/v1/appointments/available_times/?doctor_id=${this.selectedDoctor.id}&date=${this.appointmentForm.date}`)
                    .then(response => {
                        this.availableTimes = response.data.map(time => ({
                            value: time[0],
                            label: time[1],
                        }))
                    })
                    .catch(error => {
                        console.log(error)
                        this.availableTimes = [];
                    })
            }

            this.$store.commit('setIsLoading', false)
        },
        async submitAppointmentForm() {
            this.$store.commit('setIsLoading', true)

            const appointment = {
                department: this.selectedDoctor.department.id,
                doctor_id: this.selectedDoctor.id,
                ...this.appointmentForm,
            }

            await axios
                .post('/api/v1/appointments/', appointment)
                .then(response => {
                    console.log(response)

                    this.$router.push('/appointments')
                })
                .catch(error => {
                    console.log(error)
                })

            this.$store.commit('setIsLoading', false)
        },

    }
}
</script>


<style scoped>
/* Основные стили контейнера */

.department-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
    border-radius: 10px;
    background-color: #F0F8FF;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

/* Карточка отделения */
.department-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 20px rgba(30, 144, 255, 0.1);
    margin-bottom: 3rem;
    border: 1px solid rgba(30, 144, 255, 0.1);
}

/* Заголовок отделения */
.department-header {
    position: relative;
    margin-bottom: 1.5rem;
}

.department-title {
    font-size: 2rem;
    color: #1e90ff;
    margin-bottom: 0.5rem;
    font-weight: 600;
}


/* Описание отделения */
.department-description {
    color: #555;
    line-height: 1.6;
    font-size: 1.1rem;
}

/* Кнопка записи */
.appointment-btn {
    background: #1e90ff;
    color: white;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 1.5rem;
    transition: all 0.3s ease;
    font-size: 1rem;
}

.appointment-btn:hover {
    background: #187bcd;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3);
}

/* Секция врачей */
.doctors-section {
    margin-top: 2rem;
}

.doctors-title {
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-align: center;
    font-weight: 600;
    position: relative;
    padding-bottom: 0.5rem;
}

.doctors-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
}

/* Сетка врачей */
.doctors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 1rem;
}

/* Карточка врача */
.doctor-card {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(30, 144, 255, 0.1);
    transition: all 0.3s ease;
    border: 1px solid rgba(30, 144, 255, 0.1);
}

.doctor-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(30, 144, 255, 0.2);
}

/* Фото врача */
.doctor-photo-container {
    width: 100%;
    height: 250px;
    overflow: hidden;
}

.doctor-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.doctor-card:hover .doctor-photo {
    transform: scale(1.05);
}

/* Информация о враче */
.doctor-info {
    padding: 1.5rem;
    text-align: center;
}

.doctor-name {
    font-size: 1.2rem;
    color: #333;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.doctor-position {
    color: #1e90ff;
    font-weight: 500;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}

/* Кнопка записи к врачу */
.doctor-appointment-btn {
    background: #1e90ff;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 20px;
    font-size: 0.9rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    font-weight: 500;
}

.doctor-appointment-btn:hover {
    background: #187bcd;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(30, 144, 255, 0.3);
}


.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: white;
    border-radius: 10px;
    padding: 2rem;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(30, 144, 255, 0.2);
    animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.modal-content h3 {
    color: #1e90ff;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 1.5rem;
}

.field {
    margin-bottom: 1.2rem;
}

.field label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
}

.field input,
.field select,
.field textarea {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
    outline: none;
    border-color: #1e90ff;
    box-shadow: 0 0 0 2px rgba(30, 144, 255, 0.2);
}

.field textarea {
    min-height: 100px;
    resize: vertical;
}

.modal-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.button {
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
}

.button.is-success:hover {
    transform: translateY(-2px);
}


.cancel-button {
    background-color: white;
    color: #1e90ff;
    border: 1px solid #1e90ff;
    padding: 0.8rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s;
}

.cancel-button:hover {
    background-color: #f0f8ff;
    transform: translateY(-2px);
}
</style>
