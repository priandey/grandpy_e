var inputFieldElt = document.getElementById('discussField');
var responsesElt = document.getElementById('responseField');
var mapIds = []

inputFieldElt.value = "J'ai beaucoup voyagé, et j'ai plein d'histoires à te raconter !";

inputFieldElt.addEventListener("focus", function (event) {
  inputFieldElt.value = ""
  inputFieldElt.style.color = "lightgrey";
  inputFieldElt.style.textAlign = "center"
});

inputFieldElt.addEventListener("blur", function (event) {
  inputFieldElt.style.textAlign = "center"
  inputFieldElt.style.color = "lightgrey";
  inputFieldElt.value = "Poses-moi une question, mon enfant !";
});

document.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    if (inputFieldElt.value != "") {
        document.getElementById("grandpystatic").style.width = "0px";
        document.getElementById("grandpygif").style.width = "300px";
        $.post("/", {'userInput':inputFieldElt.value, 'improve_kw': ''}, postCallback);
    }
  }
 });

 function postCallback(data) {
   var requestElt = document.createElement("div");
   requestElt.textContent = inputFieldElt.value;
   requestElt.className = "col-md-8 col-xs-12 outputField";
   requestElt.id = "request";

   inputFieldElt.blur();
   inputFieldElt.style.marginTop = '2%';

   let response = JSON.parse(data);

   let responseElt = document.createElement('div');
   responseElt.className = "offset-md-4 col-md-8 col-xs-12 outputField";
   responseElt.id = "response";

   let mapElt = document.createElement('div');
   mapElt.className = "col-md-12 map";
   mapElt.id = getId(mapIds);
   mapIds.push(mapElt.id);

   responsesElt.insertBefore(responseElt, responsesElt.firstElementChild);
   responsesElt.insertBefore(requestElt, responsesElt.firstElementChild);

   if(response['status'] != 'error') {
     responseElt.textContent = "Hmmm, c'était vers "+response['address']+" si je me souviens bien. Mais t'ai-je déjà raconté que "+response['information'];
     let urlElt = document.createElement("a");
     urlElt.href = response['url'];
     urlElt.textContent = "Plus d'informations ici !";
     let weatherElt = document.createElement('div');
     weatherElt.textContent = "Selon mon cousin, MétéoBot, la température minimale est actuellement de "+response['weather']['temp_min']+"°C et la température maximale de "+response['weather']['temp_max']+"°C.";
     responseElt.appendChild(document.createElement("br"));
     responseElt.appendChild(document.createElement("br"));
     responseElt.appendChild(weatherElt);
     responseElt.appendChild(document.createElement("br"));
     responseElt.appendChild(urlElt);
     responseElt.appendChild(mapElt);
     initMap({lat: response['coordinates']['lat'], lng: response['coordinates']['long']}, mapId=mapElt.id);
   } else {
     if(response['kw'].length > 1) {
        let formElt = document.createElement("form");
        let helpMessageElt = document.createElement("p");
        helpMessageElt.textContent = "Coche les mots qui ne désignent pas un lieu, s'il te plait !";
        formElt.appendChild(helpMessageElt);
        response['kw'].forEach(function(kw) {
         let formOptElt = document.createElement("input");
         let optLabelElt = document.createElement("label");
         formOptElt.type = "checkbox";
         formOptElt.id = kw;
         formOptElt.name = "kw";
         formOptElt.value = kw;
         formOptElt.className = "formOption"
         optLabelElt.for = kw;
         optLabelElt.textContent = kw;
         formOptElt.innerHtml += " ";
         formElt.appendChild(formOptElt);
         formElt.appendChild(optLabelElt);
         formElt.appendChild(document.createElement("br"));
       });
        responseElt.appendChild(formElt);
        let sendButtonElt = document.createElement("input");
        sendButtonElt.type = "submit";
        sendButtonElt.value = "Aide ma vieille mémoire";
        formElt.appendChild(sendButtonElt);
        formElt.addEventListener('submit', improve);
      } else {
        let noOptionMessageElt = document.createElement("p");
        noOptionMessageElt.textContent = "Je ne sais pas quoi te dire, je suis un peu perdu...";
        responseElt.appendChild(noOptionMessageElt);
      }
     }

   document.getElementById("grandpystatic").style.width = "300px";
   document.getElementById("grandpygif").style.width = "0px";
   responsesElt.style.visibility = "visible";
   inputFieldElt.focus();
   inputFieldElt.blur();

 }

 function improve(event) {
   event.preventDefault();
   let kwToImprove = [];
   let kwToSearch = [];
   Array.from(document.getElementsByClassName("formOption")).forEach(function (element){
     if(element.checked === true) {
       kwToImprove.push(element.value);
     } else {
       kwToSearch.push(element.value);
     }
   });
   $.post("/", {'userInput':kwToSearch.join(" "), 'improve_kw': kwToImprove.join(" ")}, postCallback);
   inputFieldElt.value = "Le lieu c'est " + kwToSearch.join(" ");
 }

 function initMap(coord, mapId) {
   var center = coord;
   let map = new google.maps.Map(document.getElementById(mapId), {
     center: center,
     zoom: 9,
     mapTypeId: 'hybrid'
   });
   var marker = new google.maps.Marker({position: center, map:map});
 }

 function getId(IdList) {
   do {
     Id = Math.floor(Math.random() * Math.floor(1000));
    }
    while (IdList.includes(Id) === true)
    return Id.toString()
 }
