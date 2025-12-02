// favorites page
var fav1 = "Diamond Lover";
var fav2 = "Just an Encore";
var fav3 = "Intense Love";
var fav4 = "Gank Your Heart";
var fav5 = "My Little Princess";

var favList = [fav1, fav2, fav3, fav4, fav5];

var box = document.getElementById("favBox");
var button = document.getElementById("favGenerator");

if (button)
{
  button.addEventListener("click",generateFav);
}

var count = 0;

function generateFav()
{
  box.innerHTML = favList[count];
  count++;
  if (count == favList.length)
  {
    count = 0;
  }
}

// about page

var submitButton = document.getElementById("submit");
var results = document.getElementById("results");

if (submitButton)
{
  submitButton.addEventListener("click",giveSource);
}

function giveSource()
{
  var name = document.getElementById("nameInput").value;
  var source = document.getElementById("sourceInput").value.toLowerCase();
  if (source === "book")
  {
    var books = ["Harry Potter","Divergent","The Great Gatsby","Cinder"];
    var chosenBook = books[Math.floor(Math.random()*books.length)];
    results.innerHTML = name + ", you should read " + chosenBook + ".";
  }
  else if (source === "website")
  {
    var sites = ['<a href = "https://www.replit.com" target = "_blank">Replit</a>','<a href = "https://www.discord.com" target = "_blank">Discord</a>'
      ];
    var chosenSite = sites[Math.floor(Math.random()*sites.length)];
    results.innerHTML = name + ", you should go to" + chosenSite + ".";
  }
}


/*

console.log(books[2]); //book3
console.log(Math.floor(Math.random()*books.length)); //random # from 0-3 but not including 3

*/

function homeMessage()
{
  alert("Hello!");
}