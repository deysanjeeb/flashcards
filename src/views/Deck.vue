<template>
  <div class="DeCk">
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  
 <title>
   <div v-if="type === 'create'">Create Deck</div>
  <div v-if="type === 'edit'">Edit Deck</div>
  <div v-if="type === 'remove'">Remove Deck</div>
  </title>
</head>
<body>
  <div id="header">
    {{user}}
    <a href="/dashboard">Dashboard</a> | 
    <a href="/management">Deck Management</a> 
  </div>
  <br>
  {{manage_type}}
 
    <br>

        <div v-if="manage_type === 'create'">
        
        <form v-on:submit.prevent='create()' id="create-deck">
          <div>
            <label>Deck Name:</label>
            <input type="text" v-model="ndeck.deckName" required />
            </div>
            <div>
            <button type="submit">Create</button>
          </div>
        </form>

        </div>
        




        <div v-if="manage_type === 'edit'">
          <form v-on:submit.prevent='edit(deck.deck_id)' id="edit-deck">
            
            <div>
              <label>Existing Name:</label>{{deck.deck_name}}
              <br>
              <!-- <input type="hidden" id="deck" name="deckId" value={{deck.deck_id}}> -->
              <label>New Name:</label>
              <input type="text" v-model="ndeck.deckName" required />
            </div>
            <div>
              <button type="submit">Save Name</button>
            </div>
          </form>
        <a @click="editCard()" class="btn btn-primary">Edit Cards</a>
        </div>


        <div v-if="manage_type === 'remove'">
        
        <form action="http://localhost:5000/deck/remove" method="POST" id="remove-deck">
          <div>
            <label>Deck Id:</label>
            <input type="text" name="deckId" required />
          </div>
          <div>
            <input type="submit" value = "Remove">
          </div>
        </form>
        </div>

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
      ndeck:{
        deckName:null,
        deckId:null,
      },
      user:null,
      scores:null,
      decks:null,
      deck:null,
      manage_type:null,
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

        create(){
          console.log(this.ndeck.deckName)
        axios.post("http://localhost:5000/deck/create",{deckName:this.ndeck.deckName})
        .then(
          response=> {
            console.log(response);
            this.getDashboard();
            localStorage.setItem("done", this.done);
            
            this.$router.push(this.$route.query.redirect || '/management');
          },
        )
        },

        edit(deck_id){
          console.log(this.deck.deckName)
        axios.post("http://localhost:5000/edit/"+deck_id,{deckName:this.ndeck.deckName})
        .then(
          response=> {
          console.log(response);
          this.getDashboard();
          localStorage.setItem("done", this.done);
          
          this.$router.push(this.$route.query.redirect || '/management');
          },
        )
      },

      editCard(){
          console.log(this.deck.deckName)
        axios.get("http://localhost:5000/card/edit/"+this.deck.deck_id)
        .then(
          response=> {
            console.log(response);
            this.type = "all";
            this.cards = response.data.cards;
            
            localStorage.setItem("type", "all");
            localStorage.setItem("card", JSON.stringify(this.card));
            localStorage.setItem("done", this.done);
            localStorage.setItem("deck_id", this.deck.deck_id);
            this.$router.push(this.$route.query.redirect || '/card');
          },
        )
        },

      remove(card_id){
          console.log(this.card.front)
        axios.post("http://localhost:5000/card/remove",{cardId:card_id,deck_id:this.deck.deck_id})
        .then(
          response=> {
            console.log(response);
            this.type = response.data.type;
            this.cards = response.data.cards;
            
            localStorage.setItem("type", this.type);
            localStorage.setItem("cards", JSON.stringify(this.cards));
            localStorage.setItem("done", this.done);
            console.log(this.cards)
            this.$router.push(this.$route.query.redirect || '/card');
            location.reload();
          },
        )
        },
},
created(){
  this.getAuthentication();
/*  if(localStorage.getItem("manage_type")){*/
    this.manage_type = localStorage.getItem("manage_type");
    /*cards = JSON.parse(localStorage.getItem("cards"));*/
    /*if (typeof localStorage.getItem("deck") !== 'undefined'){
      console.log("caught1")
      this.deck = JSON.parse(localStorage.getItem("deck"));
    console.log("deck",this.deck);
    }*/


    
  /*}*/
},
beforeMount(){
  if(localStorage.getItem("manage_type")){
    this.manage_type = localStorage.getItem("manage_type");
    this.cards = JSON.parse(localStorage.getItem("cards"));
    this.deck = JSON.parse(localStorage.getItem("deck"));
    console.log("deck",this.deck);
  }
},
mounted(){
  if (typeof localStorage.getItem("deck") !== 'undefined'){
      console.log("caught2")
      this.deck = JSON.parse(localStorage.getItem("deck"));
    }
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
