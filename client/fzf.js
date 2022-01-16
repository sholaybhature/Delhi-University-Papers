let query = "economics";
let data;
let fuzz = 0.3;
let terms = query.split(/\s+/);
$.getJSON("final_data_ug_updated_2021.json", callData);
let regEx =
  "/(20[0-9]{2})|([I|II|III|IV]+ year)|([I|II|III|IV|V|VI|VII|VIII]+ sem)/gm";
/* Project abandoned due to the fact that DU paper naming scheme isn't systematic.
 * Lack of efficient searching algorithm, O(n^2) is expensive. Other solutions
 * provide bad results.
 */

function callData(data) {
  for (let [_, obj] of Object.entries(data)) {
    // let year_sem = obj["year and semester"];
    // let year_sem_score = year_sem ? query.score(year_sem, fuzz) : 0;
    // let paper_score = query.score(obj["paper"], fuzz);
    // let paper_score = obj["paper"].score(query, fuzz);
    let l = obj["paper"].split(/\s+/);
    // console.log(l, terms);
    let total;
    // let intersection = l.filter((e) => terms.includes(e));
    // obj.score = year_sem_score + paper_score;
    // obj.score = intersection.length;
    obj.score = total;
  }
  data.sort(function (a, b) {
    return b.score - a.score;
  });

  console.log(data);
}
