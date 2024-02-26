<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<section class="vh-100 gradient-custom">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card bg-dark text-white" style="border-radius: 1rem;">
          <div class="card-body p-5 text-center">

            <div class="mb-md-5 mt-md-4 pb-5">

              <h2 class="fw-bold mb-2 text-uppercase">Login</h2>
              <p class="text-white-50 mb-5">Please enter your login and password!</p>
              
              <form action="/user/login" method="POST" id="login">
              <div class="form-outline form-white mb-4">
                <label class="form-label" for="typeEmailX">Username</label>
                <input type="text" name="username" class="form-control form-control-lg" required/>
                
              </div>

              <div class="form-outline form-white mb-4">
                <label class="form-label" for="typePasswordX">Password</label>
                <input type="password" name="pwd" class="form-control form-control-lg" required/>
                
              </div>

             <!--   <p class="small mb-5 pb-lg-2"><a class="text-white-50" href="#!">Forgot password?</a></p>
 -->
              <button class="btn btn-outline-light btn-lg px-5" type="submit">Login</button>
            </form>
              
            </div>

            <div>
              <p class="mb-0">Don't have an account? <a href="/user/signup" class="text-white-50 fw-bold">Sign Up</a></p>
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
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
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
