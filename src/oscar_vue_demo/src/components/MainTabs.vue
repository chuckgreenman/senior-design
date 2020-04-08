<template>
  <v-card
    class="mx-auto" 
    outlined>
    <v-tabs
        fixed-tabs
        background-color="rgb(255, 67, 1)"
        dark>
        <v-tab>
        User
        </v-tab>
        <v-tab>
        SubReddit
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

                <div class="userResults">
                <v-layout row>
                    <v-flex md6>
                    <h3> Most Popular Words for {{this.user}} </h3>
                    </v-flex>
                    <v-flex md6>
                    <h3> Most Popular Links for {{this.user}} </h3>  
                    </v-flex>
                </v-layout>     

                <v-layout row>
                    <v-flex md6>
                    <v-chart :options="popularWordsChartForUser"></v-chart> 
                    </v-flex>
                    <v-flex md6>
                    <v-chart :options="popularLinksChartForUser"></v-chart>
                    </v-flex>
                </v-layout> 

                <v-layout row>
                    <v-flex md6>
                    <h3> Proportion of Controversial Posts for {{this.user}} </h3> 
                    </v-flex>     
                    <v-flex md6>
                    <h3> SubReddits that {{this.user}} Participates in </h3> 
                    </v-flex>               
                </v-layout>

                <v-layout row>
                    <v-flex md6>
                    <v-chart :options="controversyChartForUser"></v-chart> 
                    </v-flex>      
                    <v-flex md6>
                    <v-chart :options="initSubRedditRelationChartForUser"></v-chart> 
                    </v-flex>                     
                </v-layout> 

                <v-layout row>
                    <v-flex md6>
                    <h3> {{this.user}}'s Karma </h3> 
                    </v-flex> 
                    <v-flex md6>
                      <div class="databaseResults" id="dbResult1">
                        <h3> Evaluation Results</h3> 
                      </div>
                  </v-flex>                                             
                </v-layout>                     

                <v-layout row> 
                  <v-flex md6>
                    <v-chart :width="auto" :options="karmaChart"></v-chart>  
                  </v-flex>            
                  <v-flex md6>  
                    <div class="databaseResults" id="dbResult2">                  
                       <v-simple-table style="width:100%" height="300px"
                       :headers="headers"                        
                        class="elevation-1">
                          <tr height="100px">
                            <th>                              
                              <div class="tooltip">Delay Percentile
                                <span class="tooltiptext">A measurement that ranks a user's delay between 
                                  registering their account and making their first action. A value lower than 0.2 may
                                  be considered abnormal for a user.</span>
                              </div> 
                            </th>
                            <td>{{this.delay}}</td>                          
                          </tr>
                          <tr height="100px">
                            <th>                              
                              <div class="tooltip">Action Count
                                <span class="tooltiptext">A measurement that ranks a user's amount of actions taken. A 
                                  value higher than 0.8 may be considered abnormal for a user. </span>
                              </div> 
                            </th>
                            <td>{{this.action}}</td>                            
                          </tr>
                          <tr height="100px">
                            <th>                              
                              <div class="tooltip">Relationship with Closest Neighbors
                                <span class="tooltiptext">A measurement that determines similarity to other users.
                                  It is considered abnormal for a user to have many strong relationships with other users 
                                  in the subreddits they interact with.
                                </span>
                              </div> 
                            </th>
                            <td>{{this.relationshipNeighbors}}</td>                            
                          </tr>
                        </v-simple-table> 
                    </div>
                  </v-flex>                                 
                </v-layout> 

                </div>    

                </v-container>
            </v-card>
        </v-tab-item>
        <v-tab-item>          
            <v-card flat>
                <v-container>                
                <v-layout row >
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
                <div class="subRedditResults" id="subRedditResult1">
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
                    <v-flex md6>
                    <h3> SubReddits that Users of r/{{this.subreddit}} Also Post on </h3> 
                    </v-flex>               
                </v-layout>

                <v-layout row>
                    <v-flex md6>
                    <v-chart :options="controversyChart"></v-chart> 
                    </v-flex>      
                    <v-flex md6>
                    <v-chart :options="initSubRedditRelationChart"></v-chart> 
                    </v-flex>                     
                </v-layout> 

                <v-layout row>
                    <v-flex md12>
                    <h3> Popular SubReddits of r/{{this.subreddit }} Expanded Based on User's Top SubReddits to Post on </h3> 
                    </v-flex>                                             
                </v-layout>  

                <div class="subRedditResults" id="extendedChart">                  
                    <v-chart :width="auto" :options="fullSubRedditRelationChart"></v-chart>                   
                </div>

                </div>                                                          
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
    delay: null,
    action: null,
    relationshipNeighbors: null,
    popularWordsChart:  null,
    popularLinksChart: null,
    popularWordsChartForUser:  null,
    popularLinksChartForUser: null,
    controversyChart: null,
    controversyChartForUser: null,
    karmaChart : null,
    initSubRedditRelationChart: null,
    initSubRedditRelationChartForUser: null,
    fullSubRedditRelationChart: null,
    noDataAvailable: {
      title: {
          show: true,
          textStyle:{
            color:'grey',
            fontSize:20
          },
          text: 'No Data is Available',
          left: 'center',
          top: 'center'
        },
      xAxis: {
          show: false
      },
      yAxis: {
          show: false
      },
      series: []
    }
  }),
  methods: {
      // Will get user in user textfield and perform
      // http get request to flask server at 127.0.0.1      
    getUser: function () {                  
      axios.get('http://localhost:5000/user', {         
         params: { name: this.user }}, {timeout: 0})
      .then((response) => {
        var i = null;
        // Reveals elements
        // reveal elements seems to change during processing, so we use
        // a while loop to bypass
        var revealElements = document.getElementsByClassName("userResults");
        while(revealElements.item(0) != null)
        {            
            revealElements.item(0).className = "showResults";
            revealElements = document.getElementsByClassName("userResults");
        }

        revealElements = [document.getElementById("dbResult1"), document.getElementById("dbResult2")];
        // if user was present in database and results were returned, reveal
        if(response.data.evaluation != null){          
          for(i = 0; i < revealElements.length; i++)
          {            
              revealElements[i].className = "showResults";              
          }         
          if(response.data.evaluation["delay_percentile"] > 0.2)
          {
            this.delay = 'Normal';
          }
          else{
            this.delay = 'Abnormal: Delay Percentile: ' + response.data.evaluation["delay_percentile"].toString();
          }
          if(response.data.evaluation["action_count_percentile"] < 0.8)
          {
            this.action = 'Normal';
          }
          else{
            this.action = 'Abnormal: Action Count Percentile: ' + response.data.evaluation["action_count_percentile"].toString();
          }

          var close_relationship = 0;
          for (i = 0; i < response.data.evaluation["closest_users_by_relationship_weight"].length; i++){
            // if a neighbor has a weight over 0.25
            if(response.data.evaluation["closest_users_by_relationship_weight"][i][1] > 0.25){
              close_relationship = close_relationship + 1;
            }
          }

          // If a third or more neighbors go over the threshhold, trigger abnormal
          if (close_relationship >= response.data.evaluation["closest_users_by_relationship_weight"].length / 3){
            this.relationshipNeighbors = 'Abnormal: ' + close_relationship.toString() + ' close neighbors';
          }
          else{
            this.relationshipNeighbors = 'Normal';
          }
        }       
        else{
          // Make sure results are hidden
          for(i = 0; i < revealElements.length; i++)
          {            
              revealElements[i].className = "databaseResults";              
          } 
        } 
       
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

        for(i = 0; i < legend_data.length; i++){
          legend_data[i] = legend_data[i][0]; // only store the key value
        }        
        
        var series_data = [];
        // Fill series_data in expected format
        for (i = 0; i < legend_data.length; i++){
          series_data.push({value: response.data.popular_words[legend_data[i]], name: legend_data[i]});
        }

        if(series_data.length > 0){
          // Build data for popular words chart
          this.popularWordsChartForUser = {      
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
                    name: 'Most Popular Words from ' + this.user,
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
        }
        else{
          this.popularWordsChartForUser = this.noDataAvailable;
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
        for (i = 0; i < legend_data.length; i++){
          if (response.data.most_linked_websites[legend_data[i]] > 1){
            series_data.push({value: response.data.most_linked_websites[legend_data[i]], name: legend_data[i]});
          }  
        }
        
        if(series_data.length > 0){
          // Build data for popular links chart
          this.popularLinksChartForUser = {          
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
                  name: 'Most Linked to Websites from ' + this.user,
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
        }
        else{
          this.popularLinksChartForUser = this.noDataAvailable;
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

        if(series_data.length > 0){
          // Build data for popular links chart
          this.controversyChartForUser = {          
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
                  name: 'Proportion of Controversial Posts from ' + this.user,
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
        }
        else{
          this.controversyChartForUser = this.noDataAvailable;
        }        

        legend_data = ['Comment Karma', 'Link Karma'];
        series_data = [{name: legend_data[0], value: response.data.comment_karma}, 
        {name: legend_data[1], value: response.data.link_karma}];

        // Build data for popular links chart
        this.karmaChart = {          
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
                  name: this.user + ' Karma Breakdown',
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

        series_data = [['count', 'subreddit']];

        var max_value = 0; // Used for visual map in initSubRedditRelationChart
        // Fill series_data in expected format
        for (var key in response.data.top_subreddits){
          series_data.push([response.data.top_subreddits[key], key]);
          if (response.data.top_subreddits[key] > max_value){
            max_value = response.data.top_subreddits[key];
          }
        }        

        if(series_data.length > 1){
          this.initSubRedditRelationChartForUser = {
              dataset: {
                  source: series_data
              },
              grid: {containLabel: true},
              xAxis: {name: 'count'},
              yAxis: {type: 'category'},
              visualMap: {
                  orient: 'horizontal',
                  left: 'center',
                  min: 0,
                  max: max_value,
                  text: ['High Count', 'Low Count'],
                  // Map the score column to color
                  dimension: 0,
                  inRange: {
                      color: ['#1145f0', 'rgb(255, 67, 1)'] //blue to orange
                  }
              },
              series: [
                  {
                      type: 'bar',
                      encode: {
                          // Map the "count" column to X axis.
                          x: 'count',
                          // Map the "subreddit" column to Y axis
                          y: 'subreddit'
                      }
                  }
              ]
          };
        }
        else{
          this.initSubRedditRelationChartForUser = this.noDataAvailable;
        } 
      }, (error) => {
        console.log(error);
        alert(error + ". User likely does not exist");
      });                
    },
       // Will get subreddit in subreddit textfield and perform
      // http get request to flask server at 127.0.0.1      
    getSubReddit: function () {                    
      axios.get('http://localhost:5000/subreddit', {         
         params: { name: this.subreddit }}, {timeout: 0})   
      .then((response) => {                 
        // Reveals elements
        var revealElements = document.getElementsByClassName("subRedditResults");
        for(var i = 0; i < revealElements.length; i++)
        {            
            revealElements.item(i).className = "showResults";
        }
       
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

        for(i = 0; i < legend_data.length; i++){
          legend_data[i] = legend_data[i][0]; // only store the key value
        }        
        
        var series_data = [];
        // Fill series_data in expected format
        for (i = 0; i < legend_data.length; i++){
          series_data.push({value: response.data.popular_words[legend_data[i]], name: legend_data[i]});
        }

        if(series_data.length > 0){
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
        }
        else{
          this.popularWordsChart = this.noDataAvailable;
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
        for (i = 0; i < legend_data.length; i++){
          if (response.data.most_linked_websites[legend_data[i]] > 1){
            series_data.push({value: response.data.most_linked_websites[legend_data[i]], name: legend_data[i]});
          }  
        }

        if(series_data.length > 0){
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
        }
        else{
          this.popularLinksChart = this.noDataAvailable;
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
        for (i = 0; i < legend_data.length; i++){
          series_data.push({value: response.data.proportion_controversial_posts[legend_data[i]], name: legend_data[i]});
        }

        if(series_data.length > 0){
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
        }
        else{
          this.controversyChart = this.noDataAvailable;
        }         

        axios.get('http://localhost:5000/subreddit/related', {         
          params: { name: this.subreddit, create_graph: 'True' }}, {timeout: 0})
        .then((response) => {
          series_data = [['count', 'subreddit']];

        var max_value = 0; // Used for visual map in initSubRedditRelationChart
        // Fill series_data in expected format
        for (key in response.data.related_subreddits){
          series_data.push([response.data.related_subreddits[key], key]);
          if (response.data.related_subreddits[key] > max_value){
            max_value = response.data.related_subreddits[key];
          }
        }   
        
         if(series_data.length > 1){
          this.initSubRedditRelationChart = {
            dataset: {
                source: series_data
            },
            grid: {containLabel: true},
            xAxis: {name: 'count'},
            yAxis: {type: 'category'},
            visualMap: {
                orient: 'horizontal',
                left: 'center',
                min: 0,
                max: max_value,
                text: ['High Count', 'Low Count'],
                // Map the score column to color
                dimension: 0,
                inRange: {
                    color: ['#1145f0', 'rgb(255, 67, 1)'] //blue to orange
                }
            },
            series: [
                {
                    type: 'bar',
                    encode: {
                        // Map the "count" column to X axis.
                        x: 'count',
                        // Map the "subreddit" column to Y axis
                        y: 'subreddit'
                    }
                }
            ]
         };
        }
        else{
          this.initSubRedditRelationChart = this.noDataAvailable;
        }            
        
        // Reset data
        series_data = [];
        legend_data = [];
        var temp_track = {}; // Used to subreddit name to node id
        var node = null;        
        for (key in response.data.graph_weights){                
          node = {
            id: series_data.length.toString(), // Use this to get id of node being pushed
            name: key,
            value: response.data.graph_weights[key],
            symbolSize: response.data.graph_weights[key],
            label: {
            show: true
            },
            itemStyle: {
              color: 'rgb(255, 67, 1)'
            },          
            category: null
          };          

          // Track this for later use with edges
          temp_track[node.name] = node.id;

          series_data.push(node);          
        }
        
        var link = null;
        var key = null;
        var key2 = null;
        // Create links in graph
        for (key in response.data.related_graph){             
          for (key2 = 0; key2 < response.data.related_graph[key].length; key2++){            
            link = {
              id: legend_data.length.toString(),
              source: temp_track[key],
              target: temp_track[response.data.related_graph[key][key2]]
            };
            legend_data.push(link);                                    
          }          
        }

         if(series_data.length > 0){
            this.fullSubRedditRelationChart = {        
            tooltip: {},        
            animationDuration: 1500,
              animationEasingUpdate: 'quinticInOut',
              series : [
                  {
                      name: 'SubReddit Expansion',
                      type: 'graph',
                      layout: 'circular',
                      data: series_data,
                      links: legend_data,
                      //categories: categories,
                      roam: true,
                      draggable: true,
                      focusNodeAdjacency: true,
                      itemStyle: {
                          borderColor: '#fff',
                          borderWidth: 1,
                          shadowBlur: 10,
                          shadowColor: 'rgba(0, 0, 0, 0.3)'
                      },
                      label: {
                          position: 'right',
                          formatter: '{b}'
                      },
                      lineStyle: {
                          color: 'source',
                          curveness: 0.3
                      },
                      emphasis: {
                          lineStyle: {
                              width: 10
                          }
                      }
                  }
              ]
          };
        }
        else{
          this.fullSubRedditRelationChart = this.noDataAvailable;
        } 

        }, (error) => {
          console.log(error);
          alert(error);
        });

      }, (error) => {
        console.log(error);
        alert(error + ". Subreddit likely does not exist or is quarantined.");
      });                 
    }
  }  
}
</script>


<style>
.echarts {
  width: 100%;
  height: 100%;
}

#extendedChart{
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.subRedditResults{
  display: none
}

.userResults{
  display: none
}

.showResults{
  display: block
}

.subRedditInput{
  display: block
}

.databaseResults{
  display: none
}

/*https://www.w3schools.com/howto/howto_css_tooltip.asp*/

 /* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  width: 250px;
  background-color: #555;
  color: #fff;
  text-align: center;
  padding: 5px 0;
  border-radius: 6px;

  /* Position the tooltip text */
  position: absolute;
  z-index: 1;
  top: -5px;
  left: 105%; 
  margin-left: -60px;

  /* Fade in tooltip */
  opacity: 0;
  transition: opacity 0.3s;
}

/* Tooltip arrow */
.tooltip .tooltiptext::after {  
  position: absolute;
  bottom: 100%;  /* At the top of the tooltip */
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent black transparent;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
} 
</style>