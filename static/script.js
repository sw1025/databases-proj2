//Referenced W3 Schools

function registerForm(){
  const type = document.getElementById("acc_type").value;
  console.log('hi');

  const customerInput = document.querySelectorAll("#customer input");
  const agentInput = document.querySelectorAll("#agent input");
  const staffInput = document.querySelectorAll("#staff input");

  if (type === "customer")
  {
    console.log('hi1');
    document.getElementById("customer").style.display = "block";
    document.getElementById("agent").style.display = "none";
    document.getElementById("staff").style.display = "none";
    document.getElementById("pwd").style.display = "block";
    customerInput.forEach(f => f.required = true);

  }
  else if (type === "agent")
  {
    document.getElementById("agent").style.display = "block";
    document.getElementById("customer").style.display = "none";
    document.getElementById("staff").style.display = "none";
    document.getElementById("pwd").style.display = "block";
    agentInput.forEach(f => f.required = true);
  }
  else if (type === "staff") 
  {
    document.getElementById("staff").style.display = "block";
    document.getElementById("agent").style.display = "none";
    document.getElementById("customer").style.display = "none";
    document.getElementById("pwd").style.display = "block";
    staffInput.forEach(f => f.required = true);
  }
  else
  {
    console.log('hi3');
  }
}

function searchOption()
{
  console.log("1");
  const type = document.getElementById("search_select").value;
  console.log(type);
  prices = document.getElementsByClassName("togglePrice");

  for (let i = 0; i < prices.length; i++) 
  {
    if (type === "purchase") 
    {
      console.log("search1");
      prices[i].style.display = "inline";
    } 
    else
    {
      console.log("search2");
      prices[i].style.display = "none";
    }
  }

  if (type === "upcoming" || type === "purchase"){
    console.log("seartch 1")
    document.getElementById("upcoming_search").style.display = "block";
    document.getElementById("inprogress_search").style.display = "none";
  }
  else if (type === "inprogress"){
    console.log("seartch 2")
    document.getElementById("inprogress_search").style.display = "block";
    document.getElementById("upcoming_search").style.display = "none";
  }

}


// var submit = $('.submit-btn');
// var container = $('.container');

// submit.on("click", printName);

// function printName()
// {
//   event.preventDefault(); // this prevents the page from reloading!
//   var name = $('.name').val();
//   container.append(`<p> ${name}</p>`)
// }