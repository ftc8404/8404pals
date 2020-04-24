//admin.js: a proxy between the other users and the database


// a place to visualize all of the team's data into a CI/CD branch pipeline
// first off, all entries must be supplemented with a timestamp.
//Next, we do a quicksort of the entries, from newest to oldest
//entries pertain who submitted it (by email address)

//the admin will have several priviledge permissions,
//this UI allows them to control without going through the backend, (key for tournaments)

//store all of the emails in session (7 days)
let emails = [];

//we will need to get these
let mongo = require("mongo.client"); //ES6 compatible
//data is being streamed from the kafka instance
mongo.connect("127.0.0.1"); //point it to a table, and binds it to default 127.0.0.1 port

let emailsClient = mongo.use(emails);
//open up the mongodb instance and read the data
emailsClient.onConnect( (emails) => emailsClient.read(users.emails));
emailsClient.onFailure( (err) => console.log(err) ); //some quick callbacks 
emailsClient.read(users.emails);
//Oky cool, now we have the emails. Let's implement the quixsort of the time series really quick
//:) see what i did there


const defaultSortingAlgorithm = (a, b) => {
if (a < b) {
return -1;
}
if (a > b) {
return 1;
}
return 0;
};
const quickSort = (
unsortedArray,
sortingAlgorithm = defaultSortingAlgorithm
) => {
// immutable version
const sortedArray = [...unsortedArray];
const swapArrayElements = (arrayToSwap, i, j) => {
const a = arrayToSwap[i];
arrayToSwap[i] = arrayToSwap[j];
arrayToSwap[j] = a;
};
const partition = (arrayToDivide, start, end) => {
const pivot = arrayToDivide[end];
let splitIndex = start;
for (let j = start; j <= end - 1; j++) {
const sortValue = sortingAlgorithm(arrayToDivide[j], pivot);
if (sortValue === -1) {
swapArrayElements(arrayToDivide, splitIndex, j);
splitIndex++;
}
}
swapArrayElements(arrayToDivide, splitIndex, end);
return splitIndex;
};
// Recursively sort sub-arrays.
const recursiveSort = (arraytoSort, start, end) => {
// stop condition
if (start < end) {
const pivotPosition = partition(arraytoSort, start, end);
recursiveSort(arraytoSort, start, pivotPosition - 1);
recursiveSort(arraytoSort, pivotPosition + 1, end);
}
};
// Sort the entire array.
recursiveSort(sortedArray, 0, unsortedArray.length - 1);
return sortedArray;
};

//one creates dates by first doing let g1 = new Date();
// and then later saying g1.getTime()

//heres just a test to make sure it works
//randomly create some dates for us
let dates;
for(int i = 0; i < dates.length; i++) {
	dates[i] = new Date().getTime();
	setTimeout(function() {}, 100);
}

const datesSorted = quickSort(dates);
console.log(datesSorted);
//alright, so I don't know the best way to do this.
//So I've found another method. 
//Create an object with two keys id and date
//so, it stores it in a n-size array, dates

//What type of actions should the admin have
// deletes: deletes the request to send the data to the database 
// accepts: accepts the request to send the data to the database 
// changes: changes  the request to send the data to the database

function deletes(email, msg) {
	
}

function accepts(email, msg) {

}

function changes(email, msg) {
	
}

//additionally, there should be some other actions the admin should have
//such as: promoteToAdmin
//demote: stops someone from creating changes
// ban: bans someone from the webpage itself

function promoteToAdmin(email, msg) {

}

function demote(email, msg) {

}

function ban(email, msg) {

}