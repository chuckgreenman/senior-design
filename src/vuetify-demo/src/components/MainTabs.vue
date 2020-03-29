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
                <v-row>
                    <chart :options="popularWordsChart"></chart>
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
  data: () => ({
    popularWordsChart:  {
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 10,
        data: ['ff', 'gg', 'hh', 'ii', 'jj']
    },
    series: [
        {
            name: 'test1',
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
            data: [
                {value: 335, name: 'ff'},
                {value: 310, name: 'gg'},
                {value: 234, name: 'hh'},
                {value: 135, name: 'ii'},
                {value: 1548, name: 'jj'}
            ]
        }
    ]
}
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
        console.log(response);        
        console.log(response.data);
        console.log(response.data.popular_words);
      }, (error) => {
        console.log(error);
      });                 
    }
  }  
}
</script>
