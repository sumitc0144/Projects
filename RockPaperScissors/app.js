let userScore = 0;
let computerScore = 0;
let lastUserChoice = 0;
let lastCompChoice = 0;

const choices = document.querySelectorAll(".choice");
const msg = document.querySelector("#msg");

const userScoreP = document.querySelector("#user-score");
const computerScoreP = document.querySelector("#computer-score");
const lastUserChoiceP = document.querySelector("#last-user-choice");
const lastCompChoiceP = document.querySelector("#last-comp-choice");

const genCompChoice = () => {
  const options = ["rock", "paper", "scissors"];
  const randomNum = Math.floor(Math.random() * 3);
  return options[randomNum];
};

const drawGame = (userChoice) => {
  msg.innerText = `Game Was Draw! Both chose ${userChoice}`;
  msg.style.backgroundColor = "darkblue";
};

const showWinner = (userWin, userChoice, compChoice) => {
  if (userWin) {
    userScore++;
    userScoreP.innerText = userScore;
    msg.innerText = `You Win! Your ${userChoice} beats ${compChoice}`;
    msg.style.backgroundColor = "green";
  } else {
    computerScore++;
    computerScoreP.innerText = computerScore;
    msg.innerText = `You Lose! Computer's ${compChoice} beats ${userChoice}`;
    msg.style.backgroundColor = "red";
  }
};

const playGame = (userChoice) => {
  lastUserChoice = userChoice;
  const compChoice = genCompChoice();
  lastCompChoice = compChoice;

  lastUserChoiceP.innerText = `You chose: ${lastUserChoice}`;
  lastCompChoiceP.innerText = `Computer chose: ${lastCompChoice}`;

  if (userChoice === compChoice) {
    drawGame(userChoice);
  } else {
    let userWin = true;
    if (userChoice === "rock") {
      userWin = compChoice === "paper" ? false : true;
    } else if (userChoice === "paper") {
      userWin = compChoice === "scissors" ? false : true;
    } else {
      userWin = compChoice === "rock" ? false : true;
    }
    showWinner(userWin, userChoice, compChoice);
  }
};

const reset = document.querySelector("#restart");

reset.addEventListener("click", () => {
  userScore = 0;
  computerScore = 0;
  lastUserChoice = 0;
  lastCompChoice = 0;

  userScoreP.innerText = 0;
  computerScoreP.innerText = 0;
  lastUserChoiceP.innerText = "You chose: 0";
  lastCompChoiceP.innerText = "Computer chose: 0";

  msg.innerText = "Game Reset! Start Playing";
  msg.style.backgroundColor = "";
});

choices.forEach((choice) => {
  choice.addEventListener("click", () => {
    const userChoice = choice.getAttribute("id");
    playGame(userChoice);
  });
});
