#include "fit_list.h"
#include"stdio.h"
Fit_ListItem item[1000];
Fit_List::Fit_List()
{

}
void Fit_List::initialize()
{
    head=&start;
    head->previous = 0;//有头节点的
    head->size=0; //不知道给了地址能不能这样搞
    //  for(int i=0;i<1000;i++){
    //     item[i].begin_address=-1;
    //     item[i].is_allocate=0;
    //     item[i].previous=0;
    //     item[i].next=0;
    // }
    //初始化孔洞表
    one.size=4096;//这个是一个页的大小
    one.is_allocate=0;
    one.previous=head;
    one.next=0;
    one.begin_address=0;
    head->next=&one;
}

int Fit_List::size()
{
    Fit_ListItem *temp = head->next;
    int counter = 0;

    while (temp)
    {
        temp = temp->next;
        ++counter;
    }

    return counter;
}

bool Fit_List::empty()
{
    return size() == 0;
}

Fit_ListItem *Fit_List::back()
{
    Fit_ListItem *temp = head->next;
    if (!temp)
        return nullptr;

    while (temp->next)
    {
        temp = temp->next;
    }

    return temp;
}

void Fit_List::push_back(Fit_ListItem *itemPtr)
{
    Fit_ListItem *temp = back();
    if (temp == nullptr)
        temp = head;
    temp->next = itemPtr;
    itemPtr->previous = temp;
    itemPtr->next = nullptr;
}

void Fit_List::pop_back()
{
    Fit_ListItem *temp = back();
    if (temp)
    {
        temp->previous->next = nullptr;
        temp->previous = temp->next = nullptr;
    }
}

Fit_ListItem *Fit_List::front()
{
    return head->next;
}

void Fit_List::push_front(Fit_ListItem *itemPtr)
{
    Fit_ListItem *temp = head->next;
    if (temp)
    {
        temp->previous = itemPtr;
    }
    head->next = itemPtr;
    itemPtr->previous = head;
    itemPtr->next = temp;
}

void Fit_List::pop_front()
{
    Fit_ListItem *temp = head->next;
    if (temp)
    {
        if (temp->next)
        {
            temp->next->previous = head;
        }
        head->next = temp->next;
        temp->previous = temp->next = nullptr;
    }
}

void Fit_List::erase(int pos)
{
    if (pos == 0)
    {
        pop_front();
    }
    else
    {
        int length = size();
        if (pos < length)
        {
            Fit_ListItem *temp = at(pos);

            temp->previous->next = temp->next;
            if (temp->next)
            {
                temp->next->previous = temp->previous;
            }
        }
    }
}

void Fit_List::erase(Fit_ListItem *itemPtr)
{
    Fit_ListItem *temp = head->next;
    temp->begin_address=-1;
    while (temp && temp != itemPtr)
    {
        temp = temp->next;
    }

    if (temp)
    {
        temp->previous->next = temp->next;
        if (temp->next)
        {
            temp->next->previous = temp->previous;
        }
    }
}
Fit_ListItem *Fit_List::at(int pos)
{
    Fit_ListItem *temp = head->next;

    for (int i = 0; (i < pos) && temp; ++i, temp = temp->next)
    {
    }

    return temp;
}
Fit_ListItem* Fit_List::find_hole(){
    int i=0;
    while(i<1000){
        if(item[i].begin_address==-1)
        return &item[i];
        if(i==999) i=0;
        else i++;
    }
}
int Fit_List::allocate(int size)
{
    Fit_ListItem* itemPtr=find_fit(size);
    if(itemPtr==0){//这里返回-1，不等了，找不到直接算
        return -1;
    }//分配到孔和位置
    int hole_size=itemPtr->size;
    if(hole_size==size){
        itemPtr->is_allocate=1;
        return itemPtr->begin_address;
    }
    else{
       //生成一个新的孔
        Fit_ListItem* new_hole=find_hole();
       new_hole->begin_address=itemPtr->begin_address+size;
       new_hole->size=hole_size-size;
       new_hole->previous=itemPtr;
       new_hole->next=itemPtr->next;
       itemPtr->next=new_hole;
       if(new_hole->next)
       (new_hole->next)->previous=new_hole; 
       new_hole->is_allocate=0;
       itemPtr->is_allocate=1;
       itemPtr->size=size;
       return itemPtr->begin_address;
    }
}

Fit_ListItem* Fit_List::find_fit(int size)
{
    int pos = 0;
    Fit_ListItem *temp = head->next;
    while (temp&&(temp ->size<size ||temp->is_allocate==1 ))
    {
        temp = temp->next;
        ++pos;
    }

    if (temp && temp->size>=size && temp->is_allocate==0)
    {
        return temp;
    }
    else
    {
        return  0;
    }
}
Fit_ListItem* Fit_List::find_release(int start_address)
{
    int pos = 0;
    Fit_ListItem *temp = head->next;
    while (temp&&(temp ->begin_address!=start_address||temp->is_allocate==0))
    {
        temp = temp->next;
        ++pos;
    }

    if (temp && temp->begin_address==start_address && temp->is_allocate==1)
    {
        return temp;
    }
    else
    {
        return  0;
    }
}

void Fit_List::release(int start_address,int size){
    //跟分配链表里面的begin对上了，就是对应的记录
    //释放的时候要检查前后一次，看看是不是要合并了
    Fit_ListItem* itemPtr=find_release(start_address);
    if (itemPtr==0){
      printf("error\n");
    }
    //向前检查
    if(itemPtr->size<size){
        printf("error\n");
    }
    itemPtr->is_allocate=0;
    Fit_ListItem* previous=itemPtr->previous;
    Fit_ListItem* next=itemPtr->next;
    Fit_ListItem* new_hole=find_hole();
    if(itemPtr->size==size){//无碎片
    if(previous==head){
        itemPtr->is_allocate=0;
    }
    else if(previous->is_allocate==0){//与前面分区合并
        itemPtr->begin_address=previous->begin_address;
        itemPtr->size=itemPtr->size+previous->size;
        erase(previous);
    }
      if(next&&next->is_allocate==0){//与后面分区合并
        itemPtr->size=itemPtr->size+next->size;
        erase(next);
    }  
    }
    else{ //有碎片
        //合并
        if(previous!=head&&previous->is_allocate==0){
            previous->size=size+previous->size;
            //更新
            itemPtr->is_allocate=1;
            itemPtr->begin_address=itemPtr->begin_address+size;
            itemPtr->size=itemPtr->size-size;
        }else{
            new_hole->begin_address=itemPtr->begin_address;
            new_hole->size=size;
            new_hole->is_allocate=0;
            itemPtr->is_allocate=1;
            itemPtr->begin_address=itemPtr->begin_address+size;
            itemPtr->size=itemPtr->size-size;   
            new_hole->previous=previous;
            new_hole->next=itemPtr;
            previous->next=new_hole;
            itemPtr->previous=new_hole;         
        }
    }
}

void Fit_List::print_allocate(){//打印链表
    Fit_ListItem *temp = head->next;
    int counter = 0;
    printf("start address: %x\n",start_address);
    while (temp)
    {
        ++counter;
        printf("%d_hole:\n",counter);
        printf("  startAddress:%d ||",temp->begin_address);
        printf("  is_allocate:%d ||",temp->is_allocate);
        printf("  size:%d\n",temp->size);
        temp = temp->next;
    }
}
void Fit_List::clear(){
    Fit_ListItem *temp = head->next;
    while (temp)
    {
        temp->begin_address=-1;
        temp->is_allocate=0;
        temp = temp->next;
    }

}