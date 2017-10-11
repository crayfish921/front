function init($scope) {
    var loadCallback = function($scope) {
       console.log(gapi.client);
       api = gapi.client.labyrinth;
       console.log(api);
       if (document.getElementById('body'))
	   	angular.element(document.getElementById('body')).scope().init();
    }
	apiRoot = '//' + window.location.host + '/_ah/api';
	gapi.client.load('labyrinth','v1',loadCallback,apiRoot);
	
}


var labApp = angular.module('labApp', []);
labApp.controller('TextureListCtrl', function ($scope) {



  $scope.sessionId = 'qwe';
    
  $scope.textures = {
    'wall':  "image/Center001.png",
    'path':  "image/Center002.png",
    'exit':  "image/Canyon004.png",    
    'player':  "image/bosskrot.png",
    'boss' : "image/BlackDragon90.png",
  };
  $scope.player=null
  $scope.field = [];
  $scope.doFunction = function(){
	gapi.client.labyrinth.s.button({session: $scope.sessionId}).execute(function(resp) {
	  $scope.updateField(resp);
	});
  }
  
  $scope.updateField = function(resp){
  	var x;
	var y;
    for (y in resp.rows) {
	  	$scope.field[y]=resp.rows[y].cell;
	  	for(x in resp.rows[y].cell) {
	  		if (resp.rows[y].cell[x]=='player'){
	  			$scope.player={"x": x, "y": y}
			}
	  	}
  	}
  	$scope.$apply();
  }
  
  $scope.onKeypress = function($event) {
    if (document.activeElement.name != "id"){ 
	  	switch ($event.code) {
		  	case 'KeyW':
		  		direction = 'UP';
		  		break;
		  	case 'KeyD':
		  		direction = 'RIGHT';
		  		break;
		  	case 'KeyS':
		  		direction = 'DOWN';
		  		break;
		  	case 'KeyA':
		  		direction = 'LEFT';
	  	}
	  	gapi.client.labyrinth.move.click({"direction":direction, session:$scope.sessionId}).execute(function(resp) {
	      	$scope.updateField(resp);
  		});
  	}
  }
  
  $scope.move = function(x, y) {
      
     
      var direction;
       
      if(x == $scope.player.x && y == $scope.player.y){
      	console.log("CURRENT");
      }
      else if( x == $scope.player.x && y+1 == $scope.player.y){
      	direction="UP";
      }
      else if ( x == $scope.player.x && y-1 == $scope.player.y){
      	direction="DOWN";
      }
      else if (x+1 == $scope.player.x && y == $scope.player.y){
      	direction="LEFT";
      }
      else if (x-1 == $scope.player.x && y == $scope.player.y){
      	direction="RIGHT";
      }
      else{
      	console.log("NOT APPLICABLE");
      }
      console.log(direction);
      if (direction != null){
      	gapi.client.labyrinth.move.click({"direction":direction , session:$scope.sessionId}).execute(function(resp) {
      	$scope.updateField(resp);
      	});
      } 
  }
  	
});


labApp.controller('ScoreBoardCtrl', function ($scope) {
	$scope.init = function() {
		console.log(gapi.client.labyrinth);
		gapi.client.labyrinth.get.score().execute(function(resp) {
		console.log(resp);
		$scope.scores = resp.scores	
		$scope.$apply()
		});
		
	}
    
	
});
