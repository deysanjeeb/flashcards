<template>
  <div class="DeCk">
<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  
 
</head>
<body>
  <div id="header">
    {{user}}|
    <router-link to="/dashboard">Dashboard</router-link> |  
    <router-link to="/management">Deck Management</router-link> 
  </div>
  
          <div>
           
          <div v-if="type ==='all'">
             <table border=1 cellpadding="5">
          <!-- <tr>
            <th>Front</th>
            <th>Back</th>
            <th colspan=2>Action</th>
          </tr> -->
          <div v-for="card in cards" :key="card">  
          
              <tr>
                <td width=25%>{{card.front}}</td>
                <td width=25%>{{card.back}}</td>
                <td width=25%><a @click="edit(card)" class="btn btn-primary">Edit</a></td>
                <td width=25%><a @click="remove(card.card_id)" class="btn btn-danger">Remove</a></td>
              </tr>      
          
            </div>  
          
          <a @click="add()"  class="btn btn-primary">Add</a>
          </table>
        </div>

          <div v-if="type ==='edit'">
            
            <form v-on:submit.prevent='editCard(card.card_id)' method="POST" id="edit-card">
            {{this.card.front}}<input type="text" name="front" v-model="ncard.front" required><br>
            {{this.card.back}}<input type="text" name="back" v-model="ncard.back" required><br>
          <button class="btn btn-primary"  type="submit">Save</button>
        </form>
        </div>

        <div v-if="type ==='add'">
          <form v-on:submit.prevent='addCard(deck.deck_id)' method="POST" id="add-card">
            Front<input type="text" name="front" v-model="ncard.front" required><br>
            Back<input type="text" name="back" v-model="ncard.back" required><br>
          <button class="btn btn-primary"  type="submit">Add</button>
          
            <!-- <td><input type="text" name="front" v-model="ncard.front" required>hello</td>
            <td><input type="text" name="back" v-model="ncard.back" required></td>
            <td><input class="btn btn-primary" name="action" type="submit"></td> -->
        </form>
        </div>
        
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
      user:null,
      scores:null,
      decks:null,
      manage_type:null,
      ncard:{
        front:null,
        back:null,
      },
      card:{
        front:null,
        back:null,
      },
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
        
        add(){
          localStorage.setItem("type", "add");
          this.$router.push(this.$route.query.redirect || '/card');
          location.reload();
        },

      getCards(deckid){
        console.log(deckid)
        axios.get('http://localhost:5000/getcards/'+deckid)
        .then(
          response=> {
            console.log(response);
          this.cards= response.data.cards;
          console.log(this.cards);
          localStorage.setItem("cards", JSON.stringify(this.cards));
          }  
        )
        .catch(error=> console.log(error))
        },

      addCard(deck_id){
          console.log(this.deck_id)
        axios.post("http://localhost:5000/card/create",{deckid:deck_id,front:this.ncard.front,back:this.ncard.back})
        .then(
          response=> {
            console.log(response);
            this.type = response.data.type;
            localStorage.setItem("type", this.type);
            localStorage.setItem("cards", JSON.stringify(this.cards));
            this.$router.push(this.$route.query.redirect || '/card');
            location.reload();
          },
        )
        },

edit(card){
            localStorage.setItem("type", "edit");
            localStorage.setItem("card", JSON.stringify(card));
            this.$router.push(this.$route.query.redirect || '/card');
            location.reload();
        },

editCard(card_id){
          console.log(this.card.front)
        axios.post("http://localhost:5000/card/edit/"+this.deck.deck_id,{cardId:card_id,front:this.ncard.front,back:this.ncard.back})
        .then(
          response=> {
            console.log(response);
            this.type = response.data.type;
            this.cards = response.data.cards;
            
            localStorage.setItem("type", "all");
            localStorage.setItem("cards", JSON.stringify(this.cards));
            localStorage.setItem("done", this.done);
            console.log(this.cards)
            this.$router.push(this.$route.query.redirect || '/card');
            location.reload();
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
beforeMount(){
  this.getAuthentication();
  this.deck_id = localStorage.getItem("deck_id");
  this.getCards(this.deck_id);
  if(localStorage.getItem("manage_type")){
    this.manage_type = localStorage.getItem("manage_type");
    this.cards = JSON.parse(localStorage.getItem("cards"));
    this.deck = JSON.parse(localStorage.getItem("deck"));
    this.type = localStorage.getItem("type");
    console.log(this.deck.deck_name);
  }
},
mounted(){
  if((localStorage.getItem("card"))==null){
    console.log("card does not exist")
  }
  else if(this.type != "add"){
    console.log("card exists")
    this.card = JSON.parse(localStorage.getItem("card"));
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
table,td,th {
  text-align: center;
  
}
</style>
