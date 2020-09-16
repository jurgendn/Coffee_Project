const permissionType = document.cookie
  .split("; ")
  .find((row) => row.startsWith("permissionType"))
  .split("=")[1];
if (permissionType === "Owner") {
  document.getElementById("permissionType").style.display = "block";
} else {
  document.getElementById("permissionType").style.display = "none";
}

const usrName = document.cookie
  .split("; ")
  .find((row) => row.startsWith("usrname"))
  .split("=")[1];
document.getElementById("usr_name").innerHTML = usrName.substring(
  1,
  usrName.length - 1
);
