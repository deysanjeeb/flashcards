<template>
  <div class="ManageMent">
  <head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>
    Deck Management
  </title>
</head>
<body>
  <div id="header">
    {{user}}|
    <router-link to="/dashboard">Dashboard</router-link> |  
    <a href="/management">Deck Management</a>  
  </div>
  <br>
<a @click="create()" class="btn btn-primary">Create Deck</a> 
<br>
   <div v-for="deck in decks" :key="deck">
      <div class="card" style="width: 18rem;">
      <div class="card-body">
      <h5 class="card-title">{{deck.deck_name}}</h5>
      <!-- {% for score in response[2].scores %} -->
      <div v-for="score in scores" :key="score">
                    <!-- {% if score['deck_id'] == deck['deck_id'] %} -->

      <p v-if ="score.deck_id=== deck.deck_id" class="card-text">Last Score:{{score.user_score}}<br>
      Last reviewed: {{score.time}}</p>
      </div>
      <a @click="edit(deck.deck_id)" class="btn btn-primary">Edit</a>
      <a @click="remove(deck.deck_id)" class="btn btn-danger">Remove</a>
      <a @click="exprt(deck.deck_id)" class="btn">Export</a>
    </div>
      
    </div>

</div>
    <br>
  </body>
</div>
  </template>

<script>
import axios from 'axios'
export default {
  name: 'DashBoard',
  props: {
    info: []
  },
  data(){
    return{
      user:null,
      scores:null,
      decks:null,
      deck:null,
      type:null,
      card:null,
      deck_id:null,
      manage_type:null,
      formData:{
        deck_id:'',
      }
    }
  },
  methods:{

    getAuthentication(){
        const token = localStorage.getItem('jwt-token');
        axios.get('http://localhost:5000/protected',{
        headers: { 
          "Content-Type": "application/json",
          'Authorization': 'Bearer '+token
        }
        })
        .then(
          response=> {
          this.user= response.data.logged_in_as;
          localStorage.setItem("user", this.user);
          }  
        )
        .catch(error=> console.log(error))
        },
    
    getDashboard(){
        axios.get('http://localhost:5000/dashboard')
        .then(
          response=> {
            console.log(response);
          this.scores= response.data.scores;
          this.decks= response.data.decks;
          console.log(this.decks);
          localStorage.setItem("scores", JSON.stringify(this.scores));
          localStorage.setItem("decks", JSON.stringify(this.decks));
          }  
        )
        .catch(error=> console.log(error))
        },

       postData(id){
        axios.post('http://localhost:5000/review',{deck_id:id})
        .then(
          response=> {
          console.log(response);
          this.deck= response.data.deck;
          this.type= response.data.type;
          this.card= response.data.card;
          localStorage.setItem("deck", JSON.stringify(this.deck));
          localStorage.setItem("type", this.type);
          localStorage.setItem("card", JSON.stringify(this.card));
          },
          this.$router.push(this.$route.query.redirect || '/review'),
        )
        .catch(error=> console.log(error))
        },

        create(){
          localStorage.setItem("manage_type", "create");
          this.$router.push(this.$route.query.redirect || '/deck');
        },

        edit(deck_id){
        axios.get('http://localhost:5000/edit/'+deck_id)
        .then(
          response=> {
          this.manage_type= response.data.type;
          if (this.manage_type ==="add"){
            this.deck= response.data.deck;
          localStorage.setItem("type", this.manage_type);
          localStorage.setItem("deck", JSON.stringify(this.deck));
          this.$router.push(this.$route.query.redirect || '/card');
          }
          if (this.manage_type ==="edit"){
          this.cards= response.data.cards;
          this.deck= response.data.deck;
          localStorage.setItem("manage_type", this.manage_type);
          localStorage.setItem("cards", JSON.stringify(this.cards));
          localStorage.setItem("deck", JSON.stringify(this.deck));
          this.$router.push(this.$route.query.redirect || '/deck');

        }
          },
        )
        .catch(error=> console.log(error))
        },

        remove(deck_id){
        axios.get('http://localhost:5000/deck/remove/'+deck_id)
        .then(
          response=> {
            console.log(response);
          this.scores= response.data.scores;
          this.decks= response.data.decks;
          console.log(this.decks);
          localStorage.setItem("scores", this.scores);
          localStorage.setItem("decks", this.decks);
          } ,
          this.$router.push(this.$route.query.redirect || '/management'), 
        )
        .catch(error=> console.log(error))
        },

        submitForm: (formElement) => {
          let form = this.$el.querySelector(formElement)
          form.submit()
          this.editing = false
        },

        exprt: (deckid) => {
          axios.get('http://localhost:5000/deck/export/'+deckid)
        .then(
          response=> {
            console.log(response);
          this.decks= response.data.decks;
          console.log(this.decks);
          localStorage.setItem("decks", this.decks);
          } ,
          this.$router.push(this.$route.query.redirect || '/management'), 
        )
        .catch(error=> console.log(error))
        }
  
  // this.user = resp.json();
  // localStorage.setItem("user", this.user);
  // console.log("This is the data you requested", this.user);
  // return this.user;
  // },
  },
mounted(){
  this.getAuthentication();
  this.getDashboard();
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
