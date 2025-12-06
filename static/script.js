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
  else{
    console.log('hi3');
  }
}