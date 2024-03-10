var elements = {}
elements.grid = document.getElementById('grid');

elements.size = {};
elements.size.rows = document.getElementById('rows');
elements.size.columns = document.getElementById('columns');

elements.color = {};
elements.color.colorpicker = document.getElementById('colorvalue');
elements.color.coloroptions = document.getElementById('coloroptions');
elements.color.setcolor = document.getElementById('setcolor');

elements.data = {};
elements.data.output=document.getElementById('metadata');
elements.data.input=document.getElementById('metadatainput');
elements.data.loading = document.getElementById('dataloading');

elements.data.loadfile = document.getElementById('load-btn');
elements.data.savefile = document.getElementById('save-btn');

elements.animation = {};
elements.animation.add = document.getElementById('addframe');
elements.animation.frames = document.getElementById('frames');
elements.animation.timing = document.getElementById('timing');
elements.animation.repeat = document.getElementById('repeat');
elements.animation.play = document.getElementById('play');

elements.animationdata = {};
elements.animationdata.output=document.getElementById('animationdata');
elements.animationdata.input=document.getElementById('animationdatainput');
elements.animationdata.loading = document.getElementById('animationdataloading');

var rows=8;
var columns=64;

elements.size.rows.value = rows;
elements.size.columns.value = columns;
elements.size.rows.onchange = function(){
  rows=document.getElementById('rows').value;
  setGrid();
}
elements.size.columns.onchange = function(){
  columns=document.getElementById('columns').value;
  setGrid();
}
var color= elements.color.colorpicker.value;
elements.color.colorpicker.onchange = function(){
  color = elements.color.colorpicker.value;
}

function addColors(color){
  var option = document.createElement("button");
  option.style.backgroundColor = color;
  option.setAttribute("onclick","color='"+color+"';document.getElementById('colorvalue').value=color;");
  option.setAttribute("ondblclick","this.parentNode.removeChild(this);");
  option.setAttribute("class","colorchoice")
  elements.color.coloroptions.innerHTML += option.outerHTML+'  ';
}
elements.color.setcolor .setAttribute("onclick",'addColors(color);');
addColors("#ffffff");
addColors("rgb(0,0,0)");

function setGrid(){
  var pixel = document.createElement("td");
  pixel.setAttribute("onmouseover",'setPixelColour(this,false)');
  pixel.setAttribute("onmousedown",'setPixelColour(this,true);');
  pixel.style.backgroundColor='rgb(255,255,255)';
  var row = document.createElement("tr");
  row.innerHTML += (pixel.outerHTML).repeat(columns);
  
  elements.grid.innerHTML = row.outerHTML.repeat(rows);
}

var painting=false;
elements.grid.onmousedown = function(){painting=true;}
elements.grid.onmouseup = function(){painting=false;}
function setPixelColour(pixel,overwrite){  
  if (painting || overwrite){
    pixel.style.backgroundColor = color;
  }
}

setGrid();

function metadata(){
  var data = {};
  data.rows = rows;
  data.columns = columns;
  data.matrix = [];
  
  var rowslist = elements.grid.childNodes[0].childNodes;
  rowslist.forEach(function(row){
    row.childNodes.forEach(function(pixel){
      data.matrix.push(pixel.style.backgroundColor);
    });
  });
  
  return data;
}

function loadmetadata(data){
  rows = data.rows;
  columns = data.columns;
  setGrid();
  var counter = 0;
  
  var rowslist = elements.grid.childNodes[0].childNodes;
  rowslist.forEach(function(row){
    row.childNodes.forEach(function(pixel){
      pixel.style.backgroundColor = data.matrix[counter];
      counter++;
    });
  });
  
}

elements.data.output.value = JSON.stringify(metadata());
elements.data.output.onmouseover=function(){
  elements.data.output.value = JSON.stringify(metadata());
}

elements.data.loading.onclick = function(){
  alert('Loading Data:'+elements.data.input.value);
  loadmetadata(JSON.parse(
    elements.data.input.value
  ));
}

var animation = [];
function addFrame(data){
  animation.push(data);
  showFrames();
}
function removeFrame(i){
  animation.splice(i,1);
  showFrames();
}
function overwriteFrame(data,i){
  alert('Overwriting Frame '+i);
  animation[i] = data;
  showFrames();
}
function showFrames(){
  elements.animation.frames.innerHTML = '';
  for (var i=0;i<animation.length;i++){
    var option = document.createElement("button");
    option.innerHTML = i;
    option.setAttribute("onclick","loadmetadata(animation["+i+"]);");
    option.setAttribute("ondblclick","removeFrame("+i+")");
    option.setAttribute("oncontextmenu", "overwriteFrame(metadata(),"+i+")");
    //option.setAttribute("class","colorchoice")
    elements.animation.frames.innerHTML += option.outerHTML+'  ';
  }
}
elements.animation.add.setAttribute("onclick",'addFrame(metadata());');


elements.animation.timing.value = 500; //inms

function playAnimation(frame){
  if (animation.length == 0){alert("No Frames To Play!");return;}
  loadmetadata(animation[frame]);
  if (frame == animation.length-1 && elements.animation.repeat.checked){
    setTimeout(function(){playAnimation(0)}, elements.animation.timing.value);
  }
  else if (frame < animation.length){
    setTimeout(function(){playAnimation(frame+1)},elements.animation.timing.value);
  }
}
elements.animation.play.onclick = function(){playAnimation(0);}
function showAnimationData(){
  var data = {};
  data.frames = animation;
  data.timing = elements.animation.timing.value;
  data.repeat = elements.animation.repeat.checked;
  return data;
}

elements.animationdata.output.value = JSON.stringify(showAnimationData());
elements.animationdata.output.onmouseover=function(){
  elements.animationdata.output.value = JSON.stringify(showAnimationData());
}


function loadAnimationData(data){
  animation = data.frames;
  elements.animation.timing.value = data.timing;
  elements.animation.repeat.checked = data.repeat;
  showFrames();
}

elements.animationdata.loading.onclick = function(){
  alert('Loading Animation:'+elements.animationdata.input.value);
  var data = JSON.parse(
    elements.animationdata.input.value
  );
  loadAnimationData(data);
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
  } : null;
}

function parseObj(jsonData){
    
    // now the object has this structure: 
    // {"name": "PacMan", "slides": [{"buffer": [[0, 0, 0], [0, 0, 0], ... ] , "delay" : "1000"}, ...]}
    // and I need to parse it to the target form:
    // {"rows":8,"columns":8,"matrix":["rgb(255, 255, 255)","rgb(255, 255, 255)","rgb(255, 255, 255)"...]}
    //frames = jsonData.slides[0].buffer[0].length; 
    var newObj = {};
    
    newObj.frames = [];
    jsonData.slides.forEach(function(slide){
      frame = {};
      frame.rows = jsonData.fields;
      frame.columns = jsonData.columns;
      frame.matrix = [];
      //slide.buffer.forEach(function(pixel){
      //  frame.matrix.push('rgb('+pixel[0]+','+pixel[1]+','+pixel[2]+')');
      //});
      
      // this should be ok, but not, because pair columns are inverted, and inpair columns are normal, so I need to fix it
      // f.i. 0,1,2,3,4,5,6,7 is the first column, but the second is 15,14,13,12,11,10,9,8, so... it needs to be controled
      // in python I used this fix:
      /*
      for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                if i%2 == 0:
                    buffer[i*self.DIMENSION+j] = matriz_rotada[i][j]
                else:
                    buffer[i*self.DIMENSION+j] = matriz_rotada[i][self.DIMENSION-j-1]
      so I need to do the same here */
      var buffer = slide.buffer;
      for (var i=0;i<frame.rows;i++){
        for (var j=0;j<frame.columns;j++){
          //console.log(i,j,frame.columns,frame.rows,buffer[i*frame.columns+j]);
          if (i%2 == 0){
            frame.matrix[i*frame.columns+j] = 'rgb('+buffer[i*frame.columns+j][0]+','+buffer[i*frame.columns+j][1]+','+buffer[i*frame.columns+j][2]+')';
          }
          else{
            frame.matrix[i*frame.columns+j] = 'rgb('+buffer[i*frame.columns+(frame.columns-j-1)][0]+','+buffer[i*frame.columns+(frame.columns-j-1)][1]+','+buffer[i*frame.columns+(frame.columns-j-1)][2]+')';
          }
        }
      }
      // now matrix is rotated and mirrored because of the next element is order in fields, not in columns, so needs this fix
      matrix2 = [];
      for(var i=1;i<=frame.columns; i++){
        for(var j=0;j<frame.rows; j++){
          matrix2.push(frame.matrix[i-1+(j*frame.columns)]);
        }
      }
      // end fix
      frame.matrix = matrix2;

      // ok, at this point you need to check if there is a checkbox to expand the matrix, and if it's checked the background color
      if(document.getElementById("expand").checked){
        // if it's checked then you need to expand the matrix
        var newMatrix = [];
        
        var colorHex = document.getElementById("backgroundcolor").value;
        var colorRgb = hexToRgb(colorHex);

        var color = "rgb(" + colorRgb.r + "," + colorRgb.g + "," + colorRgb.b + ")";
        var checked = document.getElementById("paint").checked;

        for(var i=0;i<frame.rows;i++){
          for(var j=0;j<frame.columns;j++){
            newMatrix.push(frame.matrix[i*frame.columns+j]);
          }
          // now I need to add the background color
          var targetColumns = document.getElementById("columns").value;
          for(var j=frame.columns;j<targetColumns;j++){
            if(!checked){
              newMatrix.push('rgb(255,255,255)');
            }else{
              newMatrix.push(color);
            }
          }
        }
        frame.columns = targetColumns;
        frame.rows = frame.rows;
        frame.matrix = newMatrix;
      
      }

      newObj.frames.push(frame);
    });
    newObj.timing = jsonData.slides[0].delay;
    newObj.repeat = false;
    //console.log(newObj);
    return newObj;
}


elements.data.loadfile.onclick = function(){
  // open a dialog to select a file
  var input = document.createElement('input');
  input.type = 'file';
  // and simulate a click on it
  input.click();

  // when file is selected parse the content to json object
  input.onchange = function(){
    var file = input.files[0];
    var reader = new FileReader();
    reader.onload = function(e){
      var contents = e.target.result;
      var obj = JSON.parse(contents);
      //console.log(obj);
      // now the object has this structure: 
      // {"name": "PacMan", "slides": [{"buffer": [[0, 0, 0], [0, 0, 0], ... ] , "delay" : "1000"}, ...]}
      // and I need to parse it to the target form:
      // {"rows":8,"columns":8,"matrix":["rgb(255, 255, 255)","rgb(255, 255, 255)","rgb(255, 255, 255)"...]}
      var newObj = parseObj(obj);
      var columns = newObj.frames[0].columns;
      var rows = newObj.frames[0].rows;
      document.getElementById("columns").value = columns;
      document.getElementById("rows").value = rows;
      document.getElementById("name").value = obj.name;
      // and now I can use the newObj to load the data
      loadAnimationData(newObj);
      document.querySelector('button[onclick="loadmetadata(animation[0]);"]').click();
    };
    reader.readAsText(file);
  }

}

elements.data.savefile.onclick = function(){
  // convert the animation to the format of the file
  // first we need to reorder fields and columns in a new object
  var obj = {};
  var columns = document.getElementById("columns").value;
  var rows = document.getElementById("rows").value;
  var timing = elements.animation.timing.value;
  var slides = [];
  animation.forEach(function(frame){

    var buffer = [];
    var index2 = 0;

    for (var i = 0; i < rows; i++) {
      for(var j=0;j<columns; j++){
        var index = (i%2==0) ? (j)*rows+(i) : (columns-j)*rows-(rows-i); 
        var rgb = frame.matrix[index].replace('rgb(','').replace(')','').split(',');
        console.log((index2) + ", " + index + ", " + rgb+"p"+(i%2==0));
        buffer[index2++] = ([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
      
      }
    }
        
    slides.push({"buffer" : buffer, "delay" : timing});

  });
  obj.slides = slides;
  obj.fields = rows;
  obj.columns = columns;
  obj.name = document.getElementById("name").value;
  // now we have the object in the format of the file
  // and we need to convert it to a string to save it
  var data = JSON.stringify(obj);
  var blob = new Blob([data], {type: "text/plain"});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url;
  a.download = 'pacman.json'; // here is a TODO
  a.click();
  URL.revokeObjectURL(url);
  
}