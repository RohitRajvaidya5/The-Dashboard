let speedTestPending = false;

function showTestError(message, detail = message) {
  speedTestPending = false;
  const button = document.getElementById("speedTestBtn");
  button.classList.add("is-hidden");

  const testing = document.getElementById("testing");
  testing.classList.remove("is-loading");
  testing.innerText = message;
  testing.title = detail;
  testing.classList.remove("is-hidden");
  window.setTimeout(() => {
    if (!speedTestPending && testing.innerText === message) {
      testing.classList.add("is-hidden");
      button.classList.remove("is-hidden");
    }
  }, 2500);
}

async function updateLiveSpeeds() {
  try {
    const response = await fetch("/live");
    if (!response.ok) throw new Error("Live speed request failed");

    const data = await response.json();
    document.getElementById("download").innerText = Number(
      data.download,
    ).toFixed(2);
  } catch (error) {
    document.getElementById("download").innerText = "--";
  }
}

async function runTest() {
  const button = document.getElementById("speedTestBtn");
  const testing = document.getElementById("testing");
  button.classList.add("is-hidden");
  testing.innerText = "Testing";
  testing.classList.add("is-loading");
  testing.classList.remove("is-hidden");
  document.getElementById("speedResult").classList.add("is-hidden");

  try {
    const response = await fetch("/speedtest", { method: "POST" });
    if (!response.ok) throw new Error("Speed test request failed");

    const data = await response.json();
    if (data.message === "started" || data.message === "Speed test already running") {
      speedTestPending = true;
    } else {
      showTestError(data.message);
    }
  } catch (error) {
    showTestError("Could not start test");
  }
}

async function fetchTestResult() {
  try {
    const response = await fetch("/speedtest-result");
    if (!response.ok) throw new Error("Speed test result request failed");

    const data = await response.json();
    if (data.running) {
      speedTestPending = true;
      document.getElementById("speedTestBtn").classList.add("is-hidden");
      const testing = document.getElementById("testing");
      testing.innerText = "Testing";
      testing.classList.add("is-loading");
      testing.classList.remove("is-hidden");
      return;
    }

    if (!speedTestPending) return;

    speedTestPending = false;
    const testing = document.getElementById("testing");
    testing.classList.remove("is-loading");
    testing.classList.add("is-hidden");

    if (data.download === null || data.upload === null) {
      showTestError(
        "Test unavailable",
        data.error || "Ookla returned no valid result.",
      );
      return;
    }

    document.getElementById("maxDownload").innerText = Number(
      data.download,
    ).toFixed(2);
    document.getElementById("maxUpload").innerText = Number(
      data.upload,
    ).toFixed(2);
    const speedResult = document.getElementById("speedResult");
    speedResult.classList.remove("is-hidden");

    window.setTimeout(() => {
      speedResult.classList.add("is-hidden");
      document.getElementById("maxDownload").innerText = "0.00";
      document.getElementById("maxUpload").innerText = "0.00";
      document
        .getElementById("speedTestBtn")
        .classList.remove("is-hidden");
    }, 12000);
  } catch (error) {
    if (speedTestPending) {
      showTestError("Could not get test result");
    }
  }
}

updateLiveSpeeds();
fetchTestResult();
window.setInterval(updateLiveSpeeds, 1000);
window.setInterval(fetchTestResult, 1000);
