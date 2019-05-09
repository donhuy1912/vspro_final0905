function ExecuteScript(strId)
{
  switch (strId)
  {
      case "6Yy4M4mXRXV":
        Script1();
        break;
  }
}

function Script1()
{
  var number=Math.floor((Math.random()*6)+1);
GetPlayer().SetVar("RandomNumber",number);
}

