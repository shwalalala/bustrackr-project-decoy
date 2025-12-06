const adminCard = document.getElementById("adminCard");
  const staffCard = document.getElementById("staffCard");
 
  const usernameLabel = document.getElementById("usernameLabel");
  const usernameInput = document.getElementById("usernameInput");
  const loginBtn = document.getElementById("loginBtn");
  const selectedRoleInput = document.getElementById("selectedRole");
 
  function resetCards() {
    [adminCard, staffCard].forEach(c => c.classList.remove("ring-4", "ring-yellow-400"));
  }
 
  adminCard.addEventListener("click", () => {
    resetCards();
    adminCard.classList.add("ring-4", "ring-yellow-400");
    usernameLabel.innerText = "Admin ID";
    usernameInput.placeholder = "Admin ID";
    loginBtn.innerText = "Sign in as Admin";
    selectedRoleInput.value = "Admin";
  });
 
  staffCard.addEventListener("click", () => {
    resetCards();
    staffCard.classList.add("ring-4", "ring-yellow-400");
    usernameLabel.innerText = "Staff ID";
    usernameInput.placeholder = "Staff ID";
    loginBtn.innerText = "Sign in as Staff";
    selectedRoleInput.value = "Staff";
  });