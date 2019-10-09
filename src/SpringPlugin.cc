/*
 * Copyright 2011 Nate Koenig & Andrew Howard
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/

#include "gazebo/physics/physics.hh"
#include "SpringPlugin.hh"
#include <ros/ros.h>

using namespace gazebo;

GZ_REGISTER_MODEL_PLUGIN(SpringPlugin)

/////////////////////////////////////////////////
SpringPlugin::SpringPlugin()
{
}

/////////////////////////////////////////////////
void SpringPlugin::Load(physics::ModelPtr lmodel,
                           sdf::ElementPtr lsdf)
{
  this->model = lmodel;

  // hardcoded params for this test
  if (!lsdf->HasElement("joint_spring"))
    ROS_ERROR_NAMED("SpringPlugin","No field joint_spring for SpringPlugin");
  else
    this->jointExplicitName = lsdf->Get<std::string>("joint_spring");

  this->kpExplicit = lsdf->Get<double>("kp");

  this->kdExplicit = lsdf->Get<double>("kd");

  ROS_INFO_NAMED("SpringPlugin",
                 "Loading joint : %s kp: %f kd: %f",
                 this->jointExplicitName.c_str(),
                 this->kpExplicit,
                 this->kdExplicit);
}

/////////////////////////////////////////////////
void SpringPlugin::Init()
{
  this->jointExplicit = this->model->GetJoint(this->jointExplicitName);

  /*  this->jointImplicit->SetStiffnessDamping(0, this->kpImplicit,
      this->kdImplicit); */

  this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          boost::bind(&SpringPlugin::ExplicitUpdate, this));
}

 

/////////////////////////////////////////////////
void SpringPlugin::ExplicitUpdate()
{
  common::Time currTime = this->model->GetWorld()->GetSimTime();
  common::Time stepTime = currTime - this->prevUpdateTime;
  this->prevUpdateTime = currTime;

  double pos = this->jointExplicit->GetAngle(0).Radian();
  double vel = this->jointExplicit->GetVelocity(0);
  double force = -this->kpExplicit * pos
                 -this->kdExplicit * vel;
  this->jointExplicit->SetForce(0, force);
}

