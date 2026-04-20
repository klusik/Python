const METAR_REPORTS = Array.isArray(window.METAR_DATA) ? window.METAR_DATA : [];
const ROUND_COUNT = 10;

const DIFFICULTY_CONFIG = {
  easy: {
    label: "Easy",
    questionTypes: [
      "station",
      "windGroup",
      "visibility",
      "temperature",
      "altimeterRaw",
      "flightCategory"
    ]
  },
  medium: {
    label: "Medium",
    questionTypes: [
      "visibility",
      "temperature",
      "dewPoint",
      "windDirection",
      "windSpeed",
      "altimeterRaw",
      "observationTime",
      "weather",
      "lowestCloud",
      "ceiling",
      "flightCategory"
    ]
  },
  hard: {
    label: "Hard",
    questionTypes: [
      "dewPoint",
      "windDirection",
      "windSpeed",
      "observationTime",
      "weather",
      "lowestCloud",
      "ceiling",
      "altimeterInHg",
      "gust",
      "variableWind",
      "temperatureSpread",
      "flightCategory"
    ]
  }
};

const elements = {
  startScreen: document.getElementById("start-screen"),
  quizScreen: document.getElementById("quiz-screen"),
  resultsScreen: document.getElementById("results-screen"),
  startBtn: document.getElementById("start-btn"),
  nextBtn: document.getElementById("next-btn"),
  restartBtn: document.getElementById("restart-btn"),
  printBtn: document.getElementById("print-btn"),
  difficultyOptions: document.getElementById("difficulty-options"),
  difficultyValue: document.getElementById("difficulty-value"),
  roundLabel: document.getElementById("round-label"),
  scoreLabel: document.getElementById("score-label"),
  progressFill: document.getElementById("progress-fill"),
  metarText: document.getElementById("metar-text"),
  questionText: document.getElementById("question-text"),
  answers: document.getElementById("answers"),
  feedback: document.getElementById("feedback"),
  finalScore: document.getElementById("final-score"),
  correctCount: document.getElementById("correct-count"),
  accuracyValue: document.getElementById("accuracy-value"),
  evaluationValue: document.getElementById("evaluation-value"),
  reviewList: document.getElementById("review-list")
};

const appState = {
  rounds: [],
  currentRoundIndex: 0,
  score: 0,
  selectedDifficulty: null
};

const QUESTION_BUILDERS = {
  station: buildStationQuestion,
  windGroup: buildWindGroupQuestion,
  visibility: buildVisibilityQuestion,
  temperature: buildTemperatureQuestion,
  dewPoint: buildDewPointQuestion,
  altimeterRaw: buildAltimeterRawQuestion,
  altimeterInHg: buildAltimeterInHgQuestion,
  flightCategory: buildFlightCategoryQuestion,
  observationTime: buildObservationTimeQuestion,
  weather: buildWeatherQuestion,
  lowestCloud: buildLowestCloudQuestion,
  ceiling: buildCeilingQuestion,
  windDirection: buildWindDirectionQuestion,
  windSpeed: buildWindSpeedQuestion,
  gust: buildGustQuestion,
  variableWind: buildVariableWindQuestion,
  temperatureSpread: buildTemperatureSpreadQuestion
};

const parsedReports = METAR_REPORTS.map(parseMetar).filter(Boolean);

elements.startBtn.addEventListener("click", startQuiz);
elements.nextBtn.addEventListener("click", handleNextRound);
elements.restartBtn.addEventListener("click", returnToStart);
elements.printBtn.addEventListener("click", () => window.print());
elements.difficultyOptions.addEventListener("click", handleDifficultyClick);

setActiveScreen("start");

function handleDifficultyClick(event) {
  const button = event.target.closest("[data-level]");
  if (!button) {
    return;
  }

  appState.selectedDifficulty = button.dataset.level;
  elements.startBtn.disabled = false;
  elements.startBtn.textContent = `Start ${DIFFICULTY_CONFIG[appState.selectedDifficulty].label} Quiz`;

  [...elements.difficultyOptions.querySelectorAll(".difficulty-card")].forEach((card) => {
    card.classList.toggle("is-selected", card.dataset.level === appState.selectedDifficulty);
  });
}

function startQuiz() {
  if (!appState.selectedDifficulty) {
    return;
  }

  appState.rounds = generateRounds(appState.selectedDifficulty);
  appState.currentRoundIndex = 0;
  appState.score = 0;

  setActiveScreen("quiz");
  renderRound();
}

function returnToStart() {
  appState.selectedDifficulty = null;
  elements.startBtn.disabled = true;
  elements.startBtn.textContent = "Start Quiz";
  [...elements.difficultyOptions.querySelectorAll(".difficulty-card")].forEach((card) => {
    card.classList.remove("is-selected");
  });
  setActiveScreen("start");
}

function generateRounds(level) {
  const questionTypes = DIFFICULTY_CONFIG[level].questionTypes;
  const usageCounts = Object.fromEntries(questionTypes.map((type) => [type, 0]));
  const candidatePool = shuffle(parsedReports.map((report) => ({
    report,
    questions: questionTypes
      .map((type) => ({ type, question: QUESTION_BUILDERS[type](report) }))
      .filter((entry) => entry.question)
  }))).filter((candidate) => candidate.questions.length > 0);

  const rounds = [];

  while (rounds.length < ROUND_COUNT && candidatePool.length > 0) {
    const lowestUsage = Math.min(...questionTypes.map((type) => usageCounts[type]));
    const preferredTypes = questionTypes.filter((type) => usageCounts[type] === lowestUsage);

    let candidateIndex = candidatePool.findIndex((candidate) =>
      candidate.questions.some((entry) => preferredTypes.includes(entry.type))
    );

    if (candidateIndex === -1) {
      candidateIndex = 0;
    }

    const candidate = candidatePool.splice(candidateIndex, 1)[0];
    const minCandidateUsage = Math.min(...candidate.questions.map((entry) => usageCounts[entry.type]));
    const candidateQuestions = candidate.questions.filter((entry) => usageCounts[entry.type] === minCandidateUsage);
    const chosen = candidateQuestions[Math.floor(Math.random() * candidateQuestions.length)];

    usageCounts[chosen.type] += 1;
    rounds.push({
      report: candidate.report,
      question: chosen.question,
      answered: false,
      isCorrect: false,
      selectedOption: null
    });
  }

  return rounds.slice(0, ROUND_COUNT);
}

function renderRound() {
  const round = appState.rounds[appState.currentRoundIndex];

  elements.roundLabel.textContent = `Round ${appState.currentRoundIndex + 1} / ${ROUND_COUNT}`;
  elements.scoreLabel.textContent = String(appState.score);
  elements.progressFill.style.width = `${(appState.currentRoundIndex / ROUND_COUNT) * 100}%`;
  elements.metarText.textContent = round.report.raw;
  elements.questionText.textContent = round.question.prompt;
  elements.feedback.hidden = true;
  elements.feedback.className = "feedback";
  elements.feedback.textContent = "";
  elements.nextBtn.disabled = true;
  elements.answers.innerHTML = "";

  round.question.options.forEach((option) => {
    const button = document.createElement("button");
    button.className = "answer-btn";
    button.type = "button";
    button.textContent = option;
    button.addEventListener("click", () => submitAnswer(option));
    elements.answers.appendChild(button);
  });
}

function submitAnswer(option) {
  const round = appState.rounds[appState.currentRoundIndex];
  if (round.answered) {
    return;
  }

  round.answered = true;
  round.selectedOption = option;
  round.isCorrect = option === round.question.correct;

  if (round.isCorrect) {
    appState.score += 1;
  }

  elements.scoreLabel.textContent = String(appState.score);
  elements.progressFill.style.width = `${((appState.currentRoundIndex + 1) / ROUND_COUNT) * 100}%`;

  [...elements.answers.children].forEach((button) => {
    button.disabled = true;
    if (button.textContent === round.question.correct) {
      button.classList.add("is-correct");
    }
    if (button.textContent === option && option !== round.question.correct) {
      button.classList.add("is-wrong");
    }
  });

  elements.feedback.hidden = false;
  elements.feedback.classList.add(round.isCorrect ? "success" : "error");
  elements.feedback.textContent = round.isCorrect
    ? `Correct. ${round.question.explanation}`
    : `Incorrect. Correct answer: ${round.question.correct}. ${round.question.explanation}`;

  elements.nextBtn.disabled = false;
}

function handleNextRound() {
  if (appState.currentRoundIndex === ROUND_COUNT - 1) {
    renderResults();
    setActiveScreen("results");
    return;
  }

  appState.currentRoundIndex += 1;
  renderRound();
}

function renderResults() {
  const accuracy = Math.round((appState.score / ROUND_COUNT) * 100);

  elements.finalScore.textContent = `${appState.score} / ${ROUND_COUNT}`;
  elements.difficultyValue.textContent = DIFFICULTY_CONFIG[appState.selectedDifficulty].label;
  elements.correctCount.textContent = String(appState.score);
  elements.accuracyValue.textContent = `${accuracy}%`;
  elements.evaluationValue.textContent = getEvaluation(accuracy);
  elements.reviewList.innerHTML = "";

  appState.rounds.forEach((round, index) => {
    const item = document.createElement("article");
    item.className = "review-item";
    item.innerHTML = `
      <header>
        <strong>Round ${index + 1}</strong>
        <span class="review-badge ${round.isCorrect ? "correct" : "wrong"}">
          ${round.isCorrect ? "Correct" : "Wrong"}
        </span>
      </header>
      <p><code>${escapeHtml(round.report.raw)}</code></p>
      <p><strong>Question:</strong> ${escapeHtml(round.question.prompt)}</p>
      <p><strong>Your answer:</strong> ${escapeHtml(round.selectedOption || "-")}</p>
      <p><strong>Correct answer:</strong> ${escapeHtml(round.question.correct)}</p>
      <p><strong>Explanation:</strong> ${escapeHtml(round.question.explanation)}</p>
    `;
    elements.reviewList.appendChild(item);
  });
}

function setActiveScreen(screen) {
  elements.startScreen.classList.remove("panel-active");
  elements.quizScreen.classList.remove("panel-active");
  elements.resultsScreen.classList.remove("panel-active");

  if (screen === "start") {
    elements.startScreen.classList.add("panel-active");
  } else if (screen === "quiz") {
    elements.quizScreen.classList.add("panel-active");
  } else if (screen === "results") {
    elements.resultsScreen.classList.add("panel-active");
  }
}

function parseMetar(entry) {
  const tokens = entry.raw.trim().split(/\s+/);
  if (tokens.length < 5 || !["METAR", "SPECI"].includes(tokens[0])) {
    return null;
  }

  const station = tokens[1];
  const timeToken = tokens.find((token) => /^\d{6}Z$/.test(token)) || null;
  const timeIndex = timeToken ? tokens.indexOf(timeToken) : 1;
  const bodyTokens = tokens.slice(timeIndex + 1).filter((token) => !["AUTO", "COR"].includes(token));
  const windToken = bodyTokens.find((token) => /^(\d{3}|VRB)\d{2,3}(G\d{2,3})?(KT|MPS)$/.test(token)) || null;
  const variableWindToken = bodyTokens.find((token) => /^\d{3}V\d{3}$/.test(token)) || null;
  const visibility = extractVisibility(bodyTokens);
  const weather = extractWeather(bodyTokens);
  const tempToken = bodyTokens.find((token) => /^(M?\d{2}|\/\/)\/(M?\d{2}|\/\/)$/.test(token)) || null;
  const altimeterToken = bodyTokens.find((token) => /^A\d{4}$/.test(token)) || null;
  const cloudLayers = bodyTokens
    .filter((token) => /^(FEW|SCT|BKN|OVC|VV|CLR|SKC)\d{0,3}$/.test(token))
    .map(parseCloudLayer);
  const wind = windToken ? parseWind(windToken) : null;
  const [tempPart, dewPart] = tempToken ? tempToken.split("/") : [null, null];
  const temperatureC = tempPart ? parseSignedTemperature(tempPart) : null;
  const dewPointC = dewPart ? parseSignedTemperature(dewPart) : null;
  const ceilingFeet = decodeCeiling(cloudLayers);
  const derivedCategory = computeFlightCategory(visibility, ceilingFeet);
  const flightCategory = entry.fltCat || derivedCategory.category;

  return {
    raw: entry.raw,
    station,
    observationTime: timeToken,
    wind,
    variableWind: variableWindToken,
    visibility,
    weather,
    cloudLayers,
    lowestCloudLayer: cloudLayers[0] || null,
    ceilingFeet,
    temperatureC,
    dewPointC,
    temperatureSpreadC: temperatureC !== null && dewPointC !== null ? temperatureC - dewPointC : null,
    altimeter: altimeterToken,
    altimeterInHg: altimeterToken ? Number(`${altimeterToken.slice(1, 3)}.${altimeterToken.slice(3)}`) : null,
    flightCategory,
    flightExplanation: explainFlightCategory(flightCategory, visibility, ceilingFeet)
  };
}

function parseWind(token) {
  const match = token.match(/^(\d{3}|VRB)(\d{2,3})(G(\d{2,3}))?(KT|MPS)$/);
  if (!match) {
    return null;
  }

  return {
    raw: token,
    direction: match[1],
    speed: Number(match[2]),
    gust: match[4] ? Number(match[4]) : null,
    unit: match[5]
  };
}

function parseCloudLayer(token) {
  const match = token.match(/^(FEW|SCT|BKN|OVC|VV|CLR|SKC)(\d{3})?$/);
  if (!match) {
    return null;
  }

  return {
    raw: token,
    cover: match[1],
    baseFeet: match[2] ? Number(match[2]) * 100 : null
  };
}

function parseSignedTemperature(token) {
  if (!token || token === "//") {
    return null;
  }

  return token.startsWith("M") ? -Number(token.slice(1)) : Number(token);
}

function extractVisibility(tokens) {
  for (let index = 0; index < tokens.length; index += 1) {
    const token = tokens[index];

    if (/^(P?\d+|M?\d\/\d|\d+\/\d+)SM$/.test(token)) {
      return token;
    }
    if (/^\d+$/.test(token) && tokens[index + 1] && /^\d\/\dSM$/.test(tokens[index + 1])) {
      return `${token} ${tokens[index + 1]}`;
    }
  }

  return null;
}

function extractWeather(tokens) {
  for (const token of tokens) {
    if (/^(?:-|\+|VC)?(?:MI|PR|BC|DR|BL|SH|TS|FZ)?(?:DZ|RA|SN|SG|IC|PL|GR|GS|UP|BR|FG|FU|VA|DU|SA|HZ|PY|PO|SQ|FC|SS|DS)+$/.test(token)) {
      return token;
    }
  }

  return "No significant weather";
}

function computeFlightCategory(visibilityToken, ceilingFeet) {
  const visibilityMiles = decodeVisibility(visibilityToken);

  if ((visibilityMiles !== null && visibilityMiles < 1) || (ceilingFeet !== null && ceilingFeet < 500)) {
    return { category: "LIFR", visibilityMiles, ceilingFeet };
  }
  if ((visibilityMiles !== null && visibilityMiles < 3) || (ceilingFeet !== null && ceilingFeet < 1000)) {
    return { category: "IFR", visibilityMiles, ceilingFeet };
  }
  if ((visibilityMiles !== null && visibilityMiles <= 5) || (ceilingFeet !== null && ceilingFeet <= 3000)) {
    return { category: "MVFR", visibilityMiles, ceilingFeet };
  }
  return { category: "VFR", visibilityMiles, ceilingFeet };
}

function decodeVisibility(token) {
  if (!token) {
    return null;
  }
  if (token === "P6SM" || token === "10SM") {
    return 10;
  }

  const wholeMatch = token.match(/^(\d+)SM$/);
  if (wholeMatch) {
    return Number(wholeMatch[1]);
  }

  const simpleFractionMatch = token.match(/^M?(\d)\/(\d)SM$/);
  if (simpleFractionMatch) {
    const value = Number(simpleFractionMatch[1]) / Number(simpleFractionMatch[2]);
    return token.startsWith("M") ? value - 0.01 : value;
  }

  const compoundMatch = token.match(/^(\d+) (\d)\/(\d)SM$/);
  if (compoundMatch) {
    return Number(compoundMatch[1]) + Number(compoundMatch[2]) / Number(compoundMatch[3]);
  }

  return null;
}

function decodeCeiling(cloudLayers) {
  const ceilingLayers = cloudLayers
    .filter((layer) => layer && ["BKN", "OVC", "VV"].includes(layer.cover) && layer.baseFeet !== null)
    .map((layer) => layer.baseFeet);

  return ceilingLayers.length ? Math.min(...ceilingLayers) : null;
}

function explainFlightCategory(category, visibilityToken, ceilingFeet) {
  const parts = [];
  if (visibilityToken) {
    parts.push(`visibility ${visibilityToken}`);
  }
  if (ceilingFeet !== null) {
    parts.push(`ceiling ${ceilingFeet.toLocaleString()} ft`);
  }
  return `Official AWC category: ${category}, based on ${parts.length ? parts.join(" and ") : "reported conditions"}.`;
}

function buildStationQuestion(report) {
  return {
    prompt: "Which station issued this METAR?",
    correct: report.station,
    options: buildOptions(report.station, sampleFieldValues("station", report.station, 3)),
    explanation: `The station identifier is ${report.station}.`
  };
}

function buildWindGroupQuestion(report) {
  if (!report.wind) {
    return null;
  }

  const distractors = new Set();
  while (distractors.size < 3) {
    const direction = report.wind.direction === "VRB"
      ? "VRB"
      : offsetDirection(report.wind.direction, randomFrom([-40, -20, 20, 40, 60]));
    const speed = Math.max(0, report.wind.speed + randomFrom([-8, -5, -3, 3, 5, 8]));
    const gust = report.wind.gust
      ? `G${Math.max(speed + 2, report.wind.gust + randomFrom([-6, -4, 4, 6]))}`
      : "";
    distractors.add(`${direction}${String(speed).padStart(2, "0")}${gust}${report.wind.unit}`);
  }

  return {
    prompt: "What wind group is reported?",
    correct: report.wind.raw,
    options: buildOptions(report.wind.raw, [...distractors]),
    explanation: `The wind group in this report is ${report.wind.raw}.`
  };
}

function buildVisibilityQuestion(report) {
  if (!report.visibility) {
    return null;
  }

  return {
    prompt: "What visibility is reported?",
    correct: report.visibility,
    options: buildOptions(report.visibility, sampleFieldValues("visibility", report.visibility, 3)),
    explanation: `The reported visibility group is ${report.visibility}.`
  };
}

function buildTemperatureQuestion(report) {
  if (report.temperatureC === null) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What is the reported air temperature?",
    correctValue: report.temperatureC,
    formatter: formatTemperature,
    explanation: `The temperature/dew point group decodes to ${formatTemperature(report.temperatureC)}.`
  });
}

function buildDewPointQuestion(report) {
  if (report.dewPointC === null) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What is the reported dew point?",
    correctValue: report.dewPointC,
    formatter: formatTemperature,
    explanation: `The dew point in the temperature/dew point group is ${formatTemperature(report.dewPointC)}.`
  });
}

function buildAltimeterRawQuestion(report) {
  if (!report.altimeter) {
    return null;
  }

  return {
    prompt: "Which altimeter setting is reported?",
    correct: report.altimeter,
    options: buildOptions(report.altimeter, sampleFieldValues("altimeter", report.altimeter, 3)),
    explanation: `The altimeter group in the report is ${report.altimeter}.`
  };
}

function buildAltimeterInHgQuestion(report) {
  if (report.altimeterInHg === null) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What altimeter setting does this METAR report in inches of mercury?",
    correctValue: report.altimeterInHg,
    formatter: formatAltimeterInHg,
    offsets: [-0.21, -0.09, 0.09, 0.21, 0.14, -0.14],
    explanation: `${report.altimeter} decodes to ${formatAltimeterInHg(report.altimeterInHg)}.`
  });
}

function buildFlightCategoryQuestion(report) {
  if (!report.flightCategory) {
    return null;
  }

  return {
    prompt: "What is the flight category for this report?",
    correct: report.flightCategory,
    options: shuffle(["VFR", "MVFR", "IFR", "LIFR"]),
    explanation: report.flightExplanation
  };
}

function buildObservationTimeQuestion(report) {
  if (!report.observationTime) {
    return null;
  }

  const day = Number(report.observationTime.slice(0, 2));
  const hour = Number(report.observationTime.slice(2, 4));
  const minute = Number(report.observationTime.slice(4, 6));
  const correct = formatObservationTime(day, hour, minute);
  const distractors = new Set();

  while (distractors.size < 3) {
    const dayOffset = randomFrom([-1, 0, 0, 1]);
    const hourOffset = randomFrom([-2, -1, 1, 2]);
    const minuteOffset = randomFrom([-20, -10, 10, 20]);
    const adjusted = shiftObservationTime(day, hour, minute, dayOffset, hourOffset, minuteOffset);
    const candidate = formatObservationTime(adjusted.day, adjusted.hour, adjusted.minute);
    if (candidate !== correct) {
      distractors.add(candidate);
    }
  }

  return {
    prompt: "At what UTC day and time was this observation issued?",
    correct,
    options: buildOptions(correct, [...distractors]),
    explanation: `The time group ${report.observationTime} means day ${String(day).padStart(2, "0")} at ${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")} UTC.`
  };
}

function buildWeatherQuestion(report) {
  if (!report.weather) {
    return null;
  }

  const weatherValues = [...new Set(parsedReports.map((entry) => entry.weather).filter(Boolean))];
  const distractors = shuffle(weatherValues.filter((value) => value !== report.weather)).slice(0, 3);
  const fallbackWeather = ["-RA", "-DZ", "BR", "FG", "HZ", "TSRA", "No significant weather"];

  return {
    prompt: "Which present weather group appears in this METAR?",
    correct: report.weather,
    options: buildOptions(report.weather, distractors, fallbackWeather),
    explanation: report.weather === "No significant weather"
      ? "No present weather group appears before the cloud layers."
      : `The present weather token in the report is ${report.weather}.`
  };
}

function buildLowestCloudQuestion(report) {
  if (!report.lowestCloudLayer) {
    return null;
  }

  return {
    prompt: "What is the lowest cloud layer reported?",
    correct: report.lowestCloudLayer.raw,
    options: buildOptions(report.lowestCloudLayer.raw, sampleMappedValues(
      (entry) => entry.lowestCloudLayer ? entry.lowestCloudLayer.raw : null,
      report.lowestCloudLayer.raw,
      3
    )),
    explanation: `The first cloud layer group in the report is ${report.lowestCloudLayer.raw}.`
  };
}

function buildCeilingQuestion(report) {
  if (report.ceilingFeet === null) {
    return null;
  }

  return {
    prompt: "What is the lowest ceiling reported?",
    correct: formatCeiling(report.ceilingFeet),
    options: buildOptions(formatCeiling(report.ceilingFeet), sampleMappedValues(
      (entry) => entry.ceilingFeet !== null ? formatCeiling(entry.ceilingFeet) : null,
      formatCeiling(report.ceilingFeet),
      3
    )),
    explanation: `The lowest BKN/OVC/VV layer gives a ceiling of ${formatCeiling(report.ceilingFeet)}.`
  };
}

function buildWindDirectionQuestion(report) {
  if (!report.wind) {
    return null;
  }

  const correct = report.wind.direction === "VRB" ? "Variable" : `${report.wind.direction} deg`;
  const distractors = new Set();

  while (distractors.size < 3) {
    const candidate = report.wind.direction === "VRB"
      ? `${String(randomFrom([20, 80, 140, 220, 310])).padStart(3, "0")} deg`
      : `${offsetDirection(report.wind.direction, randomFrom([-60, -30, 30, 60, 90]))} deg`;
    if (candidate !== correct) {
      distractors.add(candidate);
    }
  }

  return {
    prompt: "What wind direction is reported?",
    correct,
    options: buildOptions(correct, [...distractors]),
    explanation: report.wind.direction === "VRB"
      ? "The wind direction group is VRB, which means variable."
      : `The wind direction is ${report.wind.direction} degrees true.`
  };
}

function buildWindSpeedQuestion(report) {
  if (!report.wind) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What sustained wind speed is reported?",
    correctValue: report.wind.speed,
    formatter: formatWindSpeed,
    offsets: [-8, -5, -3, 3, 5, 8],
    explanation: `The sustained wind speed in ${report.wind.raw} is ${formatWindSpeed(report.wind.speed)}.`
  });
}

function buildGustQuestion(report) {
  if (!report.wind || report.wind.gust === null) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What gust speed is reported?",
    correctValue: report.wind.gust,
    formatter: formatWindSpeed,
    offsets: [-10, -6, -4, 4, 6, 10],
    explanation: `The gust group in ${report.wind.raw} is ${formatWindSpeed(report.wind.gust)}.`
  });
}

function buildVariableWindQuestion(report) {
  if (!report.variableWind) {
    return null;
  }

  const start = Number(report.variableWind.slice(0, 3));
  const end = Number(report.variableWind.slice(4, 7));
  const distractors = new Set();

  while (distractors.size < 3) {
    const candidate = `${offsetDirection(start, randomFrom([-40, -20, 20, 40]))}V${offsetDirection(end, randomFrom([-40, -20, 20, 40]))}`;
    if (candidate !== report.variableWind) {
      distractors.add(candidate);
    }
  }

  return {
    prompt: "Which variable wind range is reported?",
    correct: report.variableWind,
    options: buildOptions(report.variableWind, [...distractors]),
    explanation: `The report includes the variable wind range ${report.variableWind}.`
  };
}

function buildTemperatureSpreadQuestion(report) {
  if (report.temperatureSpreadC === null) {
    return null;
  }

  return buildNumericOffsetQuestion({
    prompt: "What is the temperature-dew point spread?",
    correctValue: report.temperatureSpreadC,
    formatter: formatSpread,
    offsets: [-8, -5, -3, 3, 5, 8],
    minValue: 0,
    explanation: `${formatTemperature(report.temperatureC)} minus ${formatTemperature(report.dewPointC)} gives a spread of ${formatSpread(report.temperatureSpreadC)}.`
  });
}

function buildNumericOffsetQuestion({
  prompt,
  correctValue,
  formatter,
  explanation,
  offsets = [-8, -5, -3, 3, 5, 8],
  minValue = null
}) {
  const distractors = new Set();

  while (distractors.size < 3) {
    let candidate = correctValue + randomFrom(offsets);
    if (minValue !== null) {
      candidate = Math.max(minValue, candidate);
    }
    if (candidate !== correctValue) {
      distractors.add(formatter(candidate));
    }
  }

  return {
    prompt,
    correct: formatter(correctValue),
    options: buildOptions(formatter(correctValue), [...distractors]),
    explanation
  };
}

function sampleFieldValues(field, currentValue, count) {
  const values = parsedReports
    .map((report) => report[field])
    .filter((value) => value !== null && value !== undefined && value !== currentValue);

  return shuffle([...new Set(values)]).slice(0, count);
}

function sampleMappedValues(mapper, currentValue, count) {
  const values = parsedReports
    .map(mapper)
    .filter((value) => value !== null && value !== undefined && value !== currentValue);

  return shuffle([...new Set(values)]).slice(0, count);
}

function buildOptions(correct, distractors, fallbackOptions = []) {
  const unique = [...new Set([correct, ...distractors])];

  for (const fallback of fallbackOptions) {
    if (unique.length >= 4) {
      break;
    }
    if (fallback !== correct && !unique.includes(fallback)) {
      unique.push(fallback);
    }
  }

  return shuffle(unique.slice(0, 4));
}

function offsetDirection(direction, offset) {
  const shifted = (Number(direction) + offset + 360) % 360;
  return shifted === 0 ? "360" : String(shifted).padStart(3, "0");
}

function shiftObservationTime(day, hour, minute, dayOffset, hourOffset, minuteOffset) {
  const date = new Date(Date.UTC(2026, 3, day, hour, minute));
  date.setUTCDate(date.getUTCDate() + dayOffset);
  date.setUTCHours(date.getUTCHours() + hourOffset);
  date.setUTCMinutes(date.getUTCMinutes() + minuteOffset);

  return {
    day: date.getUTCDate(),
    hour: date.getUTCHours(),
    minute: date.getUTCMinutes()
  };
}

function formatTemperature(value) {
  return `${value} C`;
}

function formatWindSpeed(value) {
  return `${value} kt`;
}

function formatAltimeterInHg(value) {
  return `${value.toFixed(2)} inHg`;
}

function formatObservationTime(day, hour, minute) {
  return `${String(day).padStart(2, "0")} ${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}Z`;
}

function formatCeiling(value) {
  return `${value.toLocaleString()} ft`;
}

function formatSpread(value) {
  return `${value} C`;
}

function getEvaluation(accuracy) {
  if (accuracy >= 90) {
    return "Excellent";
  }
  if (accuracy >= 70) {
    return "Strong";
  }
  if (accuracy >= 50) {
    return "Fair";
  }
  return "Needs Practice";
}

function shuffle(array) {
  const copy = [...array];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}

function randomFrom(values) {
  return values[Math.floor(Math.random() * values.length)];
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
