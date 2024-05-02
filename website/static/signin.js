const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

const signInComponent = {
    template: '#signinTemplate',
    name: 'SigninComponent',
    data() {
        return {
            user: {
                email: '',
                password: ''
            }
        };
    },
    methods: {
        handleForm() {
            let formvalue = Object.assign({}, this.user);
            this.resetFormValues();
            this.$emit('signin-form', { type: 'signin', data: formvalue });
            window.location.href = '/adminDashboard'; // Redirect to Dashboard
        },
        resetFormValues() {
            this.user.email = '';
            this.user.password = '';
        },
        isValid(prop) {
            switch (prop) {
                case 'email':
                    return emailRegex.test(this.user.email);
                case 'password':
                    return this.user.password.length >= 6;
                default:
                    return false;
            }
        },
    },
    computed: {
        isFormValid() {
            return this.isValid('email') && this.isValid('password');
        }
    }
};

// Create a new Vue instance to mount the sign-in component
new Vue({
    el: '#app',
    components: {
        signin: signInComponent
    },
    data() {
        return {
            feedback: {},
            currentComponent: 'signin'
        };
    },
    methods: {
        handleForm(data) {
            this.feedback = data;
            setTimeout(() => {
                this.setComponent('feedback');
            }, 280);
        },
        isDisabled(btnName) {
            return this.currentComponent === btnName;
        },
        setComponent(componentName) {
            if (this.currentComponent !== componentName) {
                this.currentComponent = componentName;
            }
        }
    }
});
