from flask import Flask, jsonify,request

from flask_sqlalchemy import SQLAlchemy

app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/restapiflask"
app.secret_key='mysecretkey'

db = SQLAlchemy(app)

class Curso(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(30), unique=True, nullable=False)
   credits = db.Column(db.Integer, nullable=False)

   

   def __repr__(self):
      return {
         "id":self.id,
         "name ":self.name,
         "credits":self.credits
      }
   
   def serialize(self):
      return {
         "id":self.id,
         "name ":self.name,
         "credits":self.credits
      }
   


@app.route('/api/cursos' , methods=["GET"])
def listar_cursos():
   try:
      data = Curso.query.all()
      courses= [course.serialize() for course in data]
      
     
      return jsonify({'cursos':courses, 'mensaje':"Cursos listados"}),200

   except Exception as ex:
      return jsonify({'mensaje':'error'}),500


@app.route('/api/curso', methods=["GET"])
def get_course_by_name():
   try:
      namecourse = request.args["name"]
      course = Curso.query.filter_by(name=namecourse).first()
      if not course:
         return jsonify({'masg':"El curso no existe"})
      else:
         return jsonify(course.serialize()),200
   except Exception as ex:
      return jsonify({'mensaje':'error'}),500



@app.route('/api/curso', methods=["POST"])
def post_course():
   content=request.get_json(force=True)
   name = content['name']
   credits = content['credits']
   new_course = Curso(name = name, credits = credits)
   db.session.add(new_course)
   db.session.commit()

   return  jsonify(new_course.serialize())

@app.route('/api/curso', methods=["PUT"])
def put_course():
   try:
      namecourse = request.args["name"]
      edit_course = Curso.query.filter_by(name=namecourse).first()
      content=request.get_json(force=True)
      edit_course.name = content["name"]
      edit_course.credits = content["credits"]
      db.session.commit()
      if not edit_course:
         return jsonify({'masg':"El curso no existe"})
      else:
         return jsonify(edit_course.serialize()),200
   except Exception as ex:
      return jsonify({'mensaje':'error'}),500

@app.route('/api/curso', methods=["DELETE"])
def delete_course():
   try:
      namecourse = request.args["name"]
      course_deleted = Curso.query.filter_by(name=namecourse).first()
      db.session.delete(course_deleted)
      db.session.commit()
      if not course_deleted:
         return jsonify({'masg':"El curso no existe"})
      else:
         return jsonify({"course":"deleted"}),200
   except Exception as ex:
      return jsonify({'mensaje':'error'}),500


if __name__=='__main__':
   db.create_all()
   app.run(debug=True)
