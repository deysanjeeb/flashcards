<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
  
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
div id="header">
    {{user}}
    <a href="/{{user['userid']}}/dashboard">Dashboard</a> |  
    <a href="/{{user['userid']}}/deck">Deck Management</a> 
  </div>



          {% for deck in decks %}  
              <div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">{{deck['deck_name']}}</h5>
    {% for score in scores %}
                  {% if score['deck_id'] == deck['deck_id'] %}
    <p class="card-text">Last Score:{{score['user_score']}}<br>
    Last reviewed: {{score['time']}}</p>
    {% endif %}
                {% endfor %}
     <a href=/{{user['userid']}}/review/{{deck['deck_id']}} class="btn btn-primary">Review</a> 
  </div>
{% endfor %}

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
