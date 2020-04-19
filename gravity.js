/*
Gravity Simulation
*/
console.log('hello');
var canvas = document.querySelector('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
var c = canvas.getContext('2d');

var pie = Math.PI;

class Point {
    constructor(x, y){
        this.x = x;
        this.y = y;
    }

}

class Particle{
    constructor(mass, pos, velocity){
        this.x = pos.x;
        this.y = pos.y;
        this.velocity = velocity;
        this.acceleration = [0, 0];
        this.mass = mass;
        this.density = 1;
        this.radius = (3*(mass/this.density)/(4*pie))**(1/3);
        this.color = 'blue';
    }
    draw() {
        c.beginPath();
        c.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        c.strokeStyle = 'white';
        c.fillStyle = this.color;
        c.fill();
        c.stroke();
        //console.log(this.x)

    }
    UpdatePosition(others){
        let net_fx = 0;
        let net_fy = 0;

        let m1 = this.mass

        for (var i = 0; i < others.length; i++){
            if (others[i] != this) {
                let dis_x = this.x - others[i].x;
                let dis_y = this.y - others[i].y;
                let distance = Math.sqrt(dis_x**2 + dis_y**2);

                let m2 = others[i].mass;

                let alpha = Math.atan2(dis_y, dis_x);
                let gamma = 10;
                let f = (1 - m1 / (m1 + m2)) * (gamma * m1 * m2) / (distance**2);

                let fx = f*Math.cos(alpha);
                let fy = f*Math.sin(alpha);

                net_fx += fx;
                net_fy += fy;
            }
        }
        let resistance = 0.5;
        let rx = resistance*this.velocity[0];
        let ry = resistance*this.velocity[1];
        net_fx -= rx;
        net_fy -= ry;

        this.acceleration = [net_fx/m1, net_fy/m1];
        let time_step = .0003;
        this.velocity = [this.velocity[0] + this.acceleration[0]*time_step, this.velocity[1] + this.acceleration[1]*time_step];

        this.x -= this.velocity[0];
        this.y -= this.velocity[1];
    }

}

//sun
function InitializeSpace(moons_count, v0){
    var objs = [];
    let star_mass = 10000;
    let pos0 = new Point(Math.floor(canvas.width / 2), Math.floor(canvas.height / 2));
    let star = new Particle(star_mass, pos0, [0, 0]);
    star.color = 'yellow'
    objs.push(star);

    let dist_2_star = 100
    let mmass = 20
    for (let b = 0; b < moons_count; b++){
        let rang = (b+1)*360/moons_count;
        let x0 = dist_2_star*Math.cos(rang*pie/180) + Math.floor(canvas.width / 2);
        let y0 = dist_2_star*Math.sin(rang*pie/180) + Math.floor(canvas.height / 2);
        let alpha = rang - 90;
        let v_0 = [v0*Math.cos(alpha*pie/180), v0*Math.sin(alpha*pie/180)];
        let pos0 = new Point(x0, y0);
        let moon = new Particle(mmass, pos0, v_0);
        objs.push(moon);
    }
    return objs
}
function Restart(){
    var n_moons = document.getElementById('moon_num').value;
    var vel_i = document.getElementById('velocity_i').value;
    //alert(n_moons);
    objs = InitializeSpace(n_moons, vel_i);
    animate();
}
let moons_count = 2;
let v0 = .6
objs = InitializeSpace(moons_count, v0)
function animate(){
    requestAnimationFrame(animate);
    c.clearRect(0, 0, window.innerWidth, window.innerHeight);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    for (i = 0; i < objs.length; i++) {
        objs[i].draw();
        objs[i].UpdatePosition(objs);
        console.log(objs[i])

    }
}

animate();