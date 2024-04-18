#ifndef RRT_H_
#define RRT_H_

#include <cmath>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <random>
#include <vector>

struct Point {
  Point(double x, double y) : x(x), y(y) {}
  double x = 0.0;
  double y = 0.0;
};

class Node {
 public:
  Node(double x, double y) : point_(x, y), parent_(nullptr), cost_(0.0) {}
  const Point& point() const { return point_; }
  void set_parent(Node* parent) { parent_ = parent; }
  Node* parent() { return parent_; }

 private:
  Point point_; //点坐标
  std::vector<double> path_x_; 
  std::vector<double> path_y_;
  Node* parent_ = nullptr;//父节点
  double cost_ = 0.0;
};

class RRT{
  private:
    Node* start_node_;//开始节点
    Node* goal_node_;//目标节点
    std::vector<std::vector<double>> obstacle_list_;//障碍物列表
    std::vector<Node*> node_list_; //生长树中的节点
    double step_size_;//生长步长
    int goal_sample_rate_;//采样率？？不知道什么东西
    
    //生成啥的？
    std::random_device goal_rd_; //随机数生成的种子值
    std::mt19937 goal_len_;  //随机数生成器
     std::uniform_int_distribution<int> goal_dis_;//确保随机数生成的范围的

  std::random_device area_rd_;
  std::mt19937 area_gen_;
  std::uniform_real_distribution<double> area_dis_;
 public:
     RRT(Node* start_node, Node* goal_node,
      const std::vector<std::vector<double>>& obstacle_list,
      double step_size = 1.0, int goal_sample_rate = 5)
      : start_node_(start_node),
        goal_node_(goal_node),
        obstacle_list_(obstacle_list),
        step_size_(step_size),
        goal_sample_rate_(goal_sample_rate),
        goal_len_(goal_rd_()),
        goal_dis_(std::uniform_int_distribution<int>(0, 100)),//生成0-100的随机值，goal采样率是5/100，有5%的概率采样在goal
        area_gen_(area_rd_()),
        area_dis_(std::uniform_real_distribution<double>(0, 15)) {}//初始化//生成0-15的随机值
 Node* GetNearestNode(const std::vector<double>& random_position) ;//得到最近点
  bool CollisionCheck(Node*);//碰撞检测
  std::vector<Node*> Planning();//规划

};

#endif
