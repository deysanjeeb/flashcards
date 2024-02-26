<template>
  <div class="DashBoard">
    
  
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<div id="header">
    {{user}}|
    <router-link to="/dashboard">Dashboard</router-link> |  
    <router-link to="/management">Deck Management</router-link>  

          <!-- {% for deck in response[1].decks %}   -->
          <div v-for="deck in decks" :key="deck">
              <div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">{{deck.deck_name}}</h5>
    <!-- {% for score in response[2].scores %} -->
    <div v-for="score in scores" :key="score">
      <!-- {% if score['deck_id'] == deck['deck_id'] %} -->

    <div v-if ="score.deck_id === deck.deck_id" class="card-text">Last Score:{{score.user_score}}<br>
    Last reviewed: {{score.time}}
    
       <!-- <input type="hidden" v-model="formData.deck_id" value={{deck.deck_id}} > -->
       
    
  </div>

    
   <!-- <a :href="'/review/' + deck.deck_id" class="btn btn-primary">Review</a> -->
<!-- <a href=/review/{{deck.deck_id}} class="btn btn-primary">Review</a> -->
<!--  <router-link :to="{name: 'review', params: { deckid: deck.deck_id },}" class="btn btn-primary"> Review </router-link> 
 -->     
     </div>
     <form  v-on:submit.prevent="postData(deck.deck_id)">
     <button class="btn btn-primary" type="submit">
            Review
        </button>
        </form> 
   </div> 
</div>
</div>
  </div>
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
          localStorage.setItem("scores", this.scores);
          localStorage.setItem("decks", this.decks);
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

        submitForm: (formElement) => {
          let form = this.$el.querySelector(formElement)
          form.submit()
          this.editing = false
        }
  

  },
created(){
  this.getAuthentication();
  this.getDashboard();
}
}
</script>

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
