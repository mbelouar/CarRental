
const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/

const registerComponent = {
    template:'#registerTemplate',
    name:'RegisterComponent',
    data () {
        return { 
            user : {
                fullname:'',
                phone:'',
                email:'',
                address:'',
                profile:'',
                password:'',
                passwordCheck:''
            }
        }
    },
    computed: {
        isFormValid () {
            return (
                this.isValid('fullname') && 
                this.isValid('phone') && 
                this.isValid('email') && 
                this.isValid('address') &&
                this.isValid('profile') &&
                this.isValid('password') && 
                this.isValid('passwordCheck')
            )
        }
    },
    methods: {
        isValid(prop) {
            switch (prop) {
                case 'fullname':
                    return this.user.fullname.length >= 2
                    break
                case 'phone':
                    return this.user.phone.length >= 2
                    break
                case 'email':
                    return emailRegex.test(this.user.email)
                    break
                case 'address':
                    return this.user.address.length >= 2
                    break
                case 'password':
                    return this.user.password.length >= 6
                    break
                case "passwordCheck":
                    return this.user.password === this.user.passwordCheck
                    break
                case "profile":
                    return !!this.user.profile // Check if profile is selected
                default:
                    return false
            }
        },
        resetUser () {
            this.user.fullname = ''
            this.user.phone = ''
            this.user.email = ''
            this.user.address = ''
            this.user.profile = ''
            this.user.password = ''
            this.user.passwordCheck = ''
            
        },
        onSubmit () {
            let user = Object.assign({}, this.user)
            this.resetUser()
            this.$emit('register-form', {type:'register', data:user})
        }
    },
    mounted () {
        let element = this.$el.querySelector('#passwordcheck')
        element.addEventListener('blur', () => {
            if (!this.isValid('passwordCheck')) {
                element.classList.add('invalid')
            } else {
                element.classList.remove('invalid')
            }
        })  
    }
}

const signInComponent = {
    template:'#signinTemplate',
    name:'SigninComponent',
    data () {
        return { 
            user: {
                email:'',
                password:''
            }
        }
    },
    methods: {
        handleForm () {
            let formvalue = Object.assign({}, this.user)
            this.resetFormValues()
            this.$emit('signin-form', {type:'signin', data:formvalue})
            window.location.href = '/' //send Dashboard
        },
        resetFormValues () {
            this.user.email = ''
            this.user.password = ''
        },
        isValid(prop) {
            switch(prop) {
                case 'email':
                    return emailRegex.test(this.user.email)
                    break
                case 'password':
                    return this.user.password.length >= 6
                    break
                default:
                    return false
            }
        },
    },
    computed: {
        isFormValid () {
            return (this.isValid('email') && this.isValid('password'))
        }
    }
}

const feedbackComponent = {
    template:'#feedbackTemplate',
    name:"FeedbackComponent",
    filters: {
        email (input) {
            if (input.email) {
                return input.email
            } else {
                return ''
            }
        },
        name (input) {
            return input.fullname ? input.fullname : ''
        }
    },
    data () { return {} },
    props:['feedback'],
    computed: {
        title () {
            return this.feedback.type === 'signin' ?
                'Authentification done' : 'Registerd successfully'
        }
    }
}

const app = new Vue({
    el:'#app',
    components:{
        register:registerComponent,
        signin:signInComponent,
        feedback:feedbackComponent
    },
    name:'application',
    data () {
        return {
            feedback:{},
            currentComponent:'register'
        }
    },
    methods: {
        handleForm ( data ) {
            this.feedback = data
            setTimeout(() => {
                this.setComponent('feedback')
            }, 280)
        },
        isDisabled (btnName) {
            return (this.currentComponent === btnName)
        },
        setComponent(componentName) {
            if (this.currentComponent !== componentName) {
                this.currentComponent = componentName
            }
        }
    }
})