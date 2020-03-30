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
                <v-layout row>
                  <v-flex md10>
                  <v-text-field
                        label="User"
                        v-model="user"
                        single-line
                    ></v-text-field>
                  </v-flex>
                  <v-flex md2>
                  <v-btn v-on:click="getUser">Execute</v-btn>
                  </v-flex>
              </v-layout>                  
                </v-container>
            </v-card>
        </v-tab-item>
        <v-tab-item>
            <v-card flat>
                <v-container>
                <v-layout row>
                    <v-flex md10>
                    <v-text-field
                        label="SubReddit"
                        v-model="subreddit"
                        single-line
                    ></v-text-field>
                    </v-flex>
                    <v-flex md2>
                    <v-btn v-on:click="getSubReddit">Execute</v-btn>
                    </v-flex>
                </v-layout>          

                <v-layout row>
                    <v-flex md6>
                    <h3> Most Popular Words for r/{{this.subreddit}} </h3>
                    </v-flex>
                    <v-flex md6>
                    <h3> Most Popular Links for r/{{this.subreddit}} </h3>  
                    </v-flex>
                </v-layout>     

                <v-layout row>
                    <v-flex md6>
                    <v-chart :options="popularWordsChart"></v-chart> 
                    </v-flex>
                    <v-flex md6>
                    <v-chart :options="popularLinksChart"></v-chart>
                    </v-flex>
                </v-layout> 

                <v-layout row>
                    <v-flex md6>
                    <h3> Proportion of Controversial Posts on r/{{this.subreddit}} </h3> 
                    </v-flex>                    
                </v-layout>

                <v-layout row>
                    <v-flex md6>
                    <v-chart :options="controversyChart"></v-chart> 
                    </v-flex>                    
                </v-layout> 
                                              
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
  data: () => ({
    popularWordsChart:  null,
    popularLinksChart: null,
    controversyChart: null
  }),
  methods: {
      // Will get user in user textfield and perform
      // http get request to flask server at 127.0.0.1
      // TODO: Check for blank user name
    getUser: function () {                  
      axios.get('http://localhost:5000/user', {         
         params: { name: this.user }}, {timeout: 0})
      .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      });                
    },
       // Will get subreddit in subreddit textfield and perform
      // http get request to flask server at 127.0.0.1
      // TODO: Check for blank user name
    getSubReddit: function () {              
      axios.get('http://localhost:5000/subreddit', {         
         params: { name: this.subreddit }}, {timeout: 0})   

      .then((response) => {
        // Create items array
        var legend_data = Object.keys(response.data.popular_words).map(function(key) {
          return [key, response.data.popular_words[key]];
        });
        
        // Sort the array based on the second element
        legend_data.sort(function(first, second) {
          return second[1] - first[1];
        });
                
        // Create a new array with only the first 16 items taking only the keys
        legend_data = legend_data.slice(0, 16);

        for(var i = 0; i < legend_data.length; i++){
          legend_data[i] = legend_data[i][0]; // only store the key value
        }        
        
        var series_data = [];
        // Fill series_data in expected format
        for (var key in response.data.popular_words){
          series_data.push({value: response.data.popular_words[key], name: key});
        }
        // Build data for popular words chart
        this.popularWordsChart = {      
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                left: 10,                
                data: legend_data
            },
            series: [
                {
                    name: 'Most Popular Words from\n r/' + this.subreddit,
                    type: 'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: series_data
                }
            ]
        }

        // Create items array
        legend_data = Object.keys(response.data.most_linked_websites).map(function(key) {
          return [key, response.data.most_linked_websites[key]];
        });

        // Sort the array based on the second element
        legend_data.sort(function(first, second) {
          return second[1] - first[1];
        });

        // Create a new array with only the first 16 items taking only the keys
        legend_data = legend_data.slice(0, 16);
        
        for(i = 0; i < legend_data.length; i++){
          legend_data[i] = legend_data[i][0]; // only store the key value
        }

        series_data = [];
        // Fill series_data in expected format
        for (key in response.data.most_linked_websites){
          series_data.push({value: response.data.most_linked_websites[key], name: key});
        }
        // Build data for popular links chart
        this.popularLinksChart = {          
          tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
              orient: 'vertical',
              left: 10,              
              data: legend_data
          },
          series: [
              {
                  name: 'Most Linked to Websites from\n r/' + this.subreddit,
                  type: 'pie',
                  radius: ['50%', '70%'],
                  avoidLabelOverlap: false,
                  label: {
                      show: false,
                      position: 'center'
                  },
                  emphasis: {
                      label: {
                          show: true,
                          fontSize: '30',
                          fontWeight: 'bold'
                      }
                  },
                  labelLine: {
                      show: false
                  },
                  data: series_data
              }
          ]
      }

      // Create items array
        legend_data = Object.keys(response.data.proportion_controversial_posts).map(function(key) {
          return [key, response.data.proportion_controversial_posts[key]];
        });

        // Sort the array based on the second element
        legend_data.sort(function(first, second) {
          return second[1] - first[1];
        });

        // Create a new array with only the first 16 items taking only the keys
        legend_data = legend_data.slice(0, 16);
        
        for(i = 0; i < legend_data.length; i++){
          legend_data[i] = legend_data[i][0]; // only store the key value
        }

        series_data = [];
        // Fill series_data in expected format
        for (key in response.data.proportion_controversial_posts){
          series_data.push({value: response.data.proportion_controversial_posts[key], name: key});
        }
        // Build data for popular links chart
        this.controversyChart = {          
          tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
              orient: 'vertical',
              left: 10,              
              data: legend_data
          },
          series: [
              {
                  name: 'Proportion of Controversial Posts on\n r/' + this.subreddit,
                  type: 'pie',
                  radius: ['50%', '70%'],
                  avoidLabelOverlap: false,
                  label: {
                      show: false,
                      position: 'center'
                  },
                  emphasis: {
                      label: {
                          show: true,
                          fontSize: '30',
                          fontWeight: 'bold'
                      }
                  },
                  labelLine: {
                      show: false
                  },
                  data: series_data
              }
          ]
      }

      }, (error) => {
        console.log(error);
      });                 
    }
  }  
}
</script>
