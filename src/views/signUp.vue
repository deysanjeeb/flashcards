<template>
  <div class="hello">
  
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<section class="vh-100 gradient-custom">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card bg-dark text-white" style="border-radius: 1rem;">
          <div class="card-body p-5 text-center">

            <div class="mb-md-5 mt-md-4 pb-5">

              <h2 class="fw-bold mb-2 text-uppercase">Sign Up</h2>
              <p class="text-white-50 mb-5">Please register your user.</p>
              
              <form @submit='postData' >
                <div class="form-outline form-white mb-4">
                <label class="form-label" for="typeEmailX">Email</label>
                <input type="text"  v-model="signup.email" class="form-control form-control-lg" required/>
                
              </div>
              <div class="form-outline form-white mb-4">
                <label class="form-label" for="typeUserX">Username</label>
                <input type="text"  v-model="signup.user" class="form-control form-control-lg" required/>
                
              </div>

              <div class="form-outline form-white mb-4">
                <label class="form-label" for="typePasswordX">Password</label>
                <input type="text" v-model="signup.pwd" class="form-control form-control-lg" required/>
                
              </div>

             <!--   <p class="small mb-5 pb-lg-2"><a class="text-white-50" href="#!">Forgot password?</a></p>
 -->
              <button class="btn btn-outline-light btn-lg px-5" type="submit">Sign Up</button>
            </form>
              
            </div>
 </div>
        </div>
      </div>
    </div>
  </div>
</section>

  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'PostComponent',
  data(){
    return{
      signup:{
        user:null,
        pwd:null,
        email:null,
      },
      info:null,
    }
  },
  methods:{
      postData(){
        axios.post('http://localhost:5000/signup',this.signup)
        .then(
          response=> {
          // console.log(response.data.token);
          this.info= response.data.token;
          localStorage.setItem("jwt-token", response.data.token);
          },
          localStorage.setItem("back", "False"),
          this.$router.push(this.$route.query.redirect || '/dashboard'),

        )
             
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
