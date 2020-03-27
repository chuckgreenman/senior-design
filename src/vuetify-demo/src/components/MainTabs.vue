<template>
  <v-card
    class="mx-auto" 
    outlined>
    <v-tabs
        fixed-tabs
        background-color="orange"
        dark>
        <v-tab>
        User
        </v-tab>
        <v-tab>
        SubReddit
        </v-tab>
        <v-tab>
        Submission
        </v-tab>    
    
        <v-tab-item>
            <v-card flat>
                <v-container>
                <v-row>
                    <v-col>
                    <v-text-field
                        label="User"
                        v-model="user"
                        single-line
                    ></v-text-field>
                    </v-col>
                    <v-col>
                    <v-btn v-on:click="getUser">Execute</v-btn>
                    </v-col>
                </v-row>
                </v-container>
            </v-card>
        </v-tab-item>
        <v-tab-item>
            <v-card flat>
                <v-container>
                <v-row>
                    <v-col>
                    <v-text-field
                        label="SubReddit"
                        v-model="subreddit"
                        single-line
                    ></v-text-field>
                    </v-col>
                    <v-col>
                    <v-btn v-on:click="getSubReddit">Execute</v-btn>
                    </v-col>
                </v-row>
                </v-container>
            </v-card>
        </v-tab-item> 
    </v-tabs>
  </v-card>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MainTabs',
  methods: {
      // Will get user in user textfield and perform
      // http get request to flask server at 127.0.0.1
      // TODO: Check for blank user name
    getUser: function () {      
      console.log("In getUser2") 
      
      axios.get('http://localhost:5000/user', { headers: {
	  'Access-Control-Allow-Origin': '*',
	}, params: { name: this.user }}, {timeout: 0})
      .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      });            
    //   this.$http.get('http://localhost:5000/user', {params: {name: this.user}}).then(response => {
 
    //     // get body data
    //     this.someData = response.body;
    //     console.log(this.someData)
    //     }, response => {
    //     // error callback
    //     console.log('Error: ' + response.body)
    // });
    },
       // Will get subreddit in subreddit textfield and perform
      // http get request to flask server at 127.0.0.1
      // TODO: Check for blank user name
    getSubReddit: function () {    
      console.log("In getsubreddit")  
      axios.get('http://localhost:5000/subreddit', { params: { name: this.subreddit }})
      .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      });             
    //   this.$http.get('http://localhost:5000/subreddit', {params: {name: this.subreddit}}).then(response => {
 
    //     // get body data
    //     this.someData = response.body;
    //     console.log(this.someData)
    //     }, response => {
    //     // error callback
    //     console.log('Error: ' + response.body)
    // });
    }
  }  
}
</script>
