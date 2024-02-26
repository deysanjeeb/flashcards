<template>
  <div class="ReView">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<head>
  <title>
     {{user}}Review
  </title>
</head>
<body>
  <div id="header">
    <a href="/dashboard">Dashboard</a> | 
   <a href="/deck">Deck Management</a> 
  </div>
      {{this.deck.deck_name}}  Review

  <div v-if="type='review'">

          <form  v-on:submit.prevent="revealBack(card.card_id,deck.deck_id)">
            <!-- <form action="/review/{{deck.deck_id}}" method="POST" id="reveal-back"> -->
          {{card.front}}
          <p v-if = "this.back==true">
          <br>
            {{card.back}}
            <br>
            <br>
            <input type="radio" id="easy" v-model="review.rating" value="3" required>
            <label for="easy">Easy</label><br>
            <input type="radio" id="medium" v-model="review.rating" value="2">
            <label for="medium">Medium</label><br>  
            <input type="radio" id="difficult" v-model="review.rating" value="1">
            <label for="difficult">Difficult</label>
          </p>
          <br>
          
            <!-- <input type="hidden" id="card" name="cardId" value={{card.card_id}}>
            <input type="hidden" id="rev_cards" name="rev_cards" value={{rev_cards}}> -->
           
           <!-- <input type="submit" name="action" value="Show">
           <br>
              
              <input type="submit" name="action" value="Next"> -->
              <!-- <button type="submit" @click="Show">Show</button>
  <button type="submit" @click="Next">Next</button> -->
         <input type="radio" v-model="review.action" value="Show">
         Show
           <br>
              
              <input type="radio" v-model="review.action" value="Next">
              Next
              <input type="submit">
          </form> 
          </div>
</body>
</div>


</template>

<script>
import axios from 'axios'
export default {
  name: 'ReView',
  props: {
    info: []
  },
  data(){
    return{
      review:{
        rating:null,
        action:null,
      },
      user:null,
      scores:null,
      decks:null,
      cardid:null,
      deckid:null,
      deck:null,
      type:null,
      card:null,
      url:null,
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
/*    getLocalData(){
        const card = localStorage.getItem('card');
        const deck = localStorage.getItem('deck');
      },*/

    getDeck(){
      console.log(this.$route.params.deckid),
      this.deckid= this.$route.params.deckid,
      this.url = 'http://localhost:5000/review/'+ this.deckid,
        axios.get(this.url)
        .then(
          response=> {
          console.log(response.data.deck);
          this.deck= response.data.deck;
          this.type= response.data.type;
          this.card= response.data.card;
          console.log(this.deck);
          localStorage.setItem("deck", this.deck);
          localStorage.setItem("type", this.type);
          localStorage.setItem("card", this.card);
          },
          // this.$router.push(this.$route.query.redirect || '/review'),
        )
        .catch(error=> console.log(error))
        },
    
    revealBack(card_id,deckid){
        let url = 'http://localhost:5000/review/'+ deckid
        console.log(url)
        var obj1
        if (this.review.action=="Show"){
          obj1= {cardId:card_id,action:this.review.action}  
        }
        else if(this.review.action=="Next"){
          obj1= {cardId:card_id,action:this.review.action,rating:this.review.rating} 
          
        }
        /*var obj1= {cardId:card_id,action:this.review.action}*/
        /*var req = { ...obj1, ...this.review }*/
        console.log(obj1)
        axios.post(url, obj1)
        .then(
          response=> {
          console.log(response);
          this.done = response.data.done;
          localStorage.setItem("done", this.done);
          if (this.done==true){
            this.decks= response.data.decks;
            this.user=response.data.user;
            this.scores=response.data.scores;
            localStorage.setItem("decks", JSON.stringify(this.decks));
            localStorage.setItem("user", JSON.stringify(this.user));
            localStorage.setItem("scores", JSON.stringify(this.scores));  
            this.$router.push(this.$route.query.redirect || '/dashboard');
          }
          this.deck= response.data.deck;
          this.type= response.data.type;
          this.card= response.data.card;
          this.back= response.data.back;
          
          localStorage.setItem("deck", JSON.stringify(this.deck));
          localStorage.setItem("type", this.type);
          localStorage.setItem("back", this.back);
          localStorage.setItem("card", JSON.stringify(this.card));
          
          },
          this.$router.push(this.$route.query.redirect || '/review'),
        )
        .catch(error=> console.log(error))
        },
        
  },
beforeMount(){
  this.getAuthentication();
  if(localStorage.getItem("deck")){
    this.deck = JSON.parse(localStorage.getItem("deck"));
    this.card = JSON.parse(localStorage.getItem("card"));
    console.log(this.deck.deck_name);
  }
  /*this.getLocalData();*/
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
