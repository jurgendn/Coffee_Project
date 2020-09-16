const permissionType = document.cookie
  .split("; ")
  .find((row) => row.startsWith("permissionType"))
  .split("=")[1];

const ownerTag = document.getElementsByClassName("ownerPermission");
const managerTag = document.getElementsByClassName("managerPermission");

if (permissionType === "Owner") {
  for (i = 0; i < ownerTag.length; i++) {
    ownerTag[i].style.display = "block";
  }
  for (i = 0; i < managerTag.length; i++) {
    managerTag[i].style.display = "none";
  }
} else {
  for (i = 0; i < ownerTag.length; i++) {
    ownerTag[i].style.display = "none";
  }
  for (i = 0; i < managerTag.length; i++) {
    managerTag[i].style.display = "block";
  }
}
