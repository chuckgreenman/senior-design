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
                    <v-btn>Execute</v-btn>
                    </v-col>
                </v-row>
                </v-container>
            </v-card>
        </v-tab-item> 
    </v-tabs>
  </v-card>
</template>

<script>
export default {
  name: 'MainTabs',
  methods: {
      // Will get user in user textfield and perform
      // http post request to flask server at 127.0.0.1
      // TODO: Check for blank user name
    getUser: function () {
      var req = '127.0.0.1/user?name=' + this.user
      console.log(req)
    //   this.$http.get(req).then(response => {
 
    // // get body data
    // this.someData = response.body;
    // console.log(this.someData)
    // }, response => {
    // // error callback
    // console.log('Error: ' + response.body)
    // });
    }
  }  
}
</script>
