/****************************************************************
**  工程名称：YS-V0.7语音识别模块驱动程序+YS-SYN6288语音合成
**	CPU: STC11L08XE
**	晶振：22.1184MHZ
**	波特率：9600 bit/S
**	
**  作者：深圳市乐幻索尔科技有限公司
**  我们的店铺：lobot—zone.taobao.com
**  修改日期：2017.9.26
**  说明：普通模式：直接发语音识别
/***************************************************************/
#include "config.h"
/************************************************************************************/
//	nAsrStatus 用来在main主程序中表示程序运行的状态，不是LD3320芯片内部的状态寄存器
//	LD_ASR_NONE:		表示没有在作ASR识别
//	LD_ASR_RUNING：		表示LD3320正在作ASR识别中
//	LD_ASR_FOUNDOK:		表示一次识别流程结束后，有一个识别结果
//	LD_ASR_FOUNDZERO:	表示一次识别流程结束后，没有识别结果
//	LD_ASR_ERROR:		表示一次识别流程中LD3320芯片内部出现不正确的状态
/***********************************************************************************/
uint8 idata nAsrStatus=0;	
void MCU_init(); 
extern void SYN_FrameInfo(uint8_t Music,uint8_t *HZdata);
void ProcessInt0(); //识别处理函数
void delay(unsigned long uldata);
void User_handle(uint8 dat);//用户执行操作函数
void Delay200ms();
void UartInit() ;
void WaitTF0();
void runActionGroup() ;
void Led_test(void);//单片机工作指示
uint8_t G0_flag=DISABLE;//运行标志，ENABLE:运行。DISABLE:禁止运行 
sbit LED=P4^2;//信号指示灯
sbit BY_PIN = P1^1;

/***********************************************************
* 名    称： void  main(void)
* 功    能： 主函数	程序入口
* 入口参数：  
* 出口参数：
* 说    明： 					 
* 调用方法： 
**********************************************************/ 
void Sendata();
void  main(void)
{
	uint8 idata nAsrRes;
	uint8 i=0;
	Led_test();
	MCU_init();
	LD_Reset();
  UartInit();
	UartIni(); /*串口初始化*/
	delay(0x2fff);	 //稍加延时1s左右等待初始化
	nAsrStatus = LD_ASR_NONE;		//	初始状态：没有在作ASR


	while(1)
	{
		switch(nAsrStatus)
		{
			case LD_ASR_RUNING:
			case LD_ASR_ERROR:		
				break;
			case LD_ASR_NONE:
			{
				nAsrStatus=LD_ASR_RUNING;
				if (RunASR()==0)	/*	启动一次ASR识别流程：ASR初始化，ASR添加关键词语，启动ASR运算*/
				{
					SYN_FrameInfo(0,"错误");
					nAsrStatus = LD_ASR_ERROR;
				}
				break;
			}
			case LD_ASR_FOUNDOK: /*	一次ASR识别流程结束，去取ASR识别结果*/
			{				
				nAsrRes = LD_GetResult();		/*获取结果*/
				User_handle(nAsrRes);//用户执行函数 
				nAsrStatus = LD_ASR_NONE;
				
				break;
			}
			case LD_ASR_FOUNDZERO:
			default:
			{
				nAsrStatus = LD_ASR_NONE;
				break;
			}
		} 			
	}

}
/***********************************************************
* 名    称： 	 LED灯测试
* 功    能： 单片机是否工作指示
* 入口参数： 无 
* 出口参数：无
* 说    明： 					 
**********************************************************/
void Led_test(void)
{
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
}
/***********************************************************
* 名    称： void MCU_init()
* 功    能： 单片机初始化
* 入口参数：  
* 出口参数：
* 说    明： 					 
* 调用方法： 
**********************************************************/ 
void MCU_init()
{
	P0 = 0xff;
	P1 = 0xff;
	P2 = 0xff;
	P3 = 0xff;
	P4 = 0xff;
	LD_MODE = 0;		//	设置MD管脚为低，并行模式读写
	IE0=1;
	EX0=1;
	EA=1;
}
/***********************************************************
* 名    称：	延时函数
* 功    能：
* 入口参数：  
* 出口参数：
* 说    明： 					 
* 调用方法： 
**********************************************************/ 
void Delay200us()		//@22.1184MHz
{
	unsigned char i, j;
	_nop_();
	_nop_();
	i = 5;
	j = 73;
	do
	{
		while (--j);
	} while (--i);
}

void  delay(unsigned long uldata)
{
	unsigned int j  =  0;
	unsigned int g  =  0;
	for (j=0;j<5;j++)
	{
		for (g=0;g<uldata;g++)
		{
			_nop_();
			_nop_();
			_nop_();
		}
	}
}

void Delay200ms()		//@22.1184MHz
{
	unsigned char i, j, k;

	i = 17;
	j = 208;
	k = 27;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}
void Delay100ms()		//@22.1184MHz
{
	unsigned char i, j, k;

	i = 9;
	j = 100;
	k = 14;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}
/***********************************************************
* 名    称： 中断处理函数
* 功    能：
* 入口参数：  
* 出口参数：
* 说    明： 					 
* 调用方法： 
**********************************************************/

void ExtInt0Handler(void) interrupt 0  
{ 	
	ProcessInt0();				/*	LD3320 送出中断信号，包括ASR和播放MP3的中断，需要在中断处理函数中分别处理*/
}
/***********************************************************
* 名    称：软串口发送数据函数
* 功    能：
* 入口参数：  
* 出口参数：
* 说    明： 					 
* 调用方法：
************************************************************/
typedef unsigned char uchar;
int i;
uchar code info[] = {0x55,0x55,0x05,0x06,0x01,0x01,0x00};
sbit newTXD = P1^0;//模拟串口的发送端设为P1.0
void UartInit()
{
	AUXR |= 0x40;		//定时器时钟1T模式
	TMOD &= 0x0F;		//设置定时器模式
	TMOD |= 0x10;		//设置定时器模式
	TL1 = 0x04;		//设置定时初值
	TH1 = 0xF7;		//设置定时初值
	TF1 = 0;		//清除TF1标志

}
void WaitTF0(void)
{
  while(!TF1);
  TF1=0;
	TL1 = 0x04;		//设置定时初值
	TH1 = 0xF7;		//设置定时初值
}
void WByte(uchar input)
{
     //发送启始位
     uchar j=8;
	   newTXD=(bit)0;
     TR1=1;
    
     WaitTF0();
     //发送8位数据位
     while(j--)
     {
         newTXD=(bit)(input&0x01);      //先传低位
         WaitTF0();
         input=input>>1;
     }

     //发送校验位(无)

     //发送结束位
     newTXD=(bit)1;
     WaitTF0();
     TR1=0;	 
}    
void Sendata(uint8_t *dat, uint8_t len)
{
		int i = 0;
     for(i=0;i<len;i++)//外层循环，遍历数组
    {
          WByte(dat[i]);
     }
}
/********************动作组调用函数*************************/
void stopActionGroup()
{
	volatile  uint8_t buf[4];
	buf[0] = 0x55 ;
	buf[1] = 0x55 ;
	buf[2] = 2 ;
	buf[3] = 0x07 ;
	PrintCom(buf, 4) ;
}
void runActionGroup(uint8_t numofAction, uint16_t Times)
{
	static volatile  uint8_t buf[7];
	buf[0] = 0x55 ;
	buf[1] = 0x55 ;
	buf[2] = 5 ;
	buf[3] = 0x06 ;
	buf[4] = (uint8_t)numofAction ;
	buf[5] = GET_LOW_BYTE(Times) ;
	buf[6] = GET_HIGH_BYTE((uint16_t)Times) ;
	PrintCom(buf, 7) ;
	
	Delay200ms();
	Delay200ms();
	Delay200ms();
}
void runXRcmd(uint8_t numofAction,uint8_t Times)
{
	UARTSendByte(0xff);
	UARTSendByte(0x05);
	UARTSendByte(numofAction);
	UARTSendByte(Times);
	UARTSendByte(0xff);
	LED = !LED;
	
	Delay100ms(); 	
SYN_FrameInfo(0,"[v14] ");

}

/***********************************************************
* 名    称：用户执行函数 
* 功    能：识别成功后，执行动作可在此进行修改 
* 入口参数： 无 
* 出口参数：无
* 说    明： 					 
**********************************************************/
void 	User_handle(uint8 dat)
{

			 switch(dat)		   /*对结果执行相关操作,客户修改*/
			  {
				   
			  	   case 1:	 
						    runXRcmd(1,1);		
							SYN_FrameInfo(0,"[v14]干啥");
							break;
				  case 2:	
							runXRcmd(3,1);
							SYN_FrameInfo(0,"是小影同学啊");
						  break;
				  case 3:	 
							SYN_FrameInfo(0,"谁说我不帅");
							runActionGroup(3,1);
							break;
					case 4:	 
							SYN_FrameInfo(0,"那当然了");
							runActionGroup(4,1);
							break;
					case 5:	 
							SYN_FrameInfo(0,"我长得那么萌，人见人爱，哈哈");
							runActionGroup(5,1);
							break;
					case 6:	 
						  SYN_FrameInfo(0,"在哪里，在哪里");
							runActionGroup(6,1);6
							break;
					case 7:	 
					    SYN_FrameInfo(0,"没看到啊");
					    runActionGroup(7,1);
							break;
					case 8:
							SYN_FrameInfo(0,"你好无聊");
							runActionGroup(8,1);
							break;
					case 9:	 
							SYN_FrameInfo(0,"你说");
							runActionGroup(9,1);
							break;
					case 10:
					 		runXRcmd(3,1);	
							SYN_FrameInfo(0,"[v14] ");	
							Delay200ms();
							SYN_FrameInfo(0,"我有女朋友，很可爱哦");						
							break;
					case 11:	 
							SYN_FrameInfo(0,"谁说我笨！我可聪明了");
							runActionGroup(11,1);
							break;
					case 12:
							SYN_FrameInfo(0,"嗯，你说");
							runActionGroup(12,1);
							break;
					case 13:	 
							SYN_FrameInfo(0,"1.414");
							runActionGroup(13,1);
							break;
					case 14:	
							SYN_FrameInfo(0,"4.47");						
							runActionGroup(14,1);
							break;
					case 15:	 
							SYN_FrameInfo(0,"那必须的，我可是大天才");
							runActionGroup(15,1);
							break;
					case 16:	 
							runActionGroup(16,1);
							break;
					case 17:	 
							SYN_FrameInfo(0,"我没有胳膊没有腿，打个毛篮球啊");
							runActionGroup(17,1);
							break;
					case 18:
							runXRcmd(4,1);	
							SYN_FrameInfo(0,"[v14] ");	
							Delay100ms();
							SYN_FrameInfo(0,"人家也不知道喔");
							break;
					case 19:	 
							SYN_FrameInfo(0,"你逗我呢");
							runActionGroup(19,1);
							break;
					case 20:	
							SYN_FrameInfo(0,"大家再见，不要想我哦");						
							runActionGroup(20,1);
							break;
					default:
						SYN_FrameInfo(0,"你这是为难我小爱");
					  runActionGroup(2,1);
				}	
				BY_PIN = 1;
				while(BY_PIN);
}	 